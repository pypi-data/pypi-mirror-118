# coding: utf-8
# cython: language_level=3, linetrace=True

"""Bindings to Prodigal, an ORF finder for genomes, progenomes and metagenomes.
"""

# ----------------------------------------------------------------------------

cimport libc.errno
from libc.stdio cimport printf
from libc.stdlib cimport malloc, free, qsort
from libc.string cimport memchr, memcmp, memcpy, memset, strcpy, strstr
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
from cpython.unicode cimport PyUnicode_DecodeASCII

from pyrodigal.prodigal cimport bitmap, dprog, gene, node, sequence
from pyrodigal.prodigal.bitmap cimport bitmap_t
from pyrodigal.prodigal.gene cimport MAX_GENES, _gene
from pyrodigal.prodigal.metagenomic cimport NUM_META, _metagenomic_bin, initialize_metagenomic_bins
from pyrodigal.prodigal.node cimport _node
from pyrodigal.prodigal.sequence cimport calc_most_gc_frame, gc_content, _mask
from pyrodigal.prodigal.training cimport _training
from pyrodigal._utils cimport _mini_training
from pyrodigal._unicode cimport *


# ----------------------------------------------------------------------------

import warnings
import threading

# ----------------------------------------------------------------------------

cdef size_t MIN_SINGLE_GENOME = 20000
cdef size_t IDEAL_SINGLE_GENOME = 100000
cdef size_t MIN_GENES = 8
cdef size_t MIN_NODES = MIN_GENES * 8

_TRANSLATION_TABLES = set((*range(1, 7), *range(9, 17), *range(21, 26)))

# ----------------------------------------------------------------------------

cdef int sequence_to_bitmap(
    object text,
    bitmap_t* seq,
    bitmap_t* rseq,
    bitmap_t* useq
) except 1:
    """Create bitmaps from a textual sequence in ``text``.

    Arguments:
        text (byte buffer): A byte buffer storing the sequence.
            Characters other than 'ATGC' or 'atgc' will be ignored and added
            to the ``useq`` bitmap.
        seq (bitmap_t*): An address where to put the bitmap storing the
          sequence.
        rseq (bitmap_t*): An address where to put the bitmap storing the
          reverse complement.
        useq (bitmap_t*): An address where to put the bitmap storing the
          *unknown character* bitmap.

    """
    # allocate memory for the bitmaps
    cdef size_t slen = len(text)
    cdef size_t blen = slen//4 + (slen%4 != 0)
    cdef size_t ulen = slen//8 + (slen%8 != 0)
    seq[0] = <bitmap_t> PyMem_Malloc(blen * sizeof(unsigned char))
    rseq[0] = <bitmap_t> PyMem_Malloc(blen * sizeof(unsigned char))
    useq[0] = <bitmap_t> PyMem_Malloc(ulen * sizeof(unsigned char))
    if not seq[0] or not useq[0] or not rseq[0]:
        PyMem_Free(seq[0])
        PyMem_Free(rseq[0])
        PyMem_Free(useq[0])
        raise MemoryError()

    # clear memory
    memset(seq[0], 0,  blen * sizeof(unsigned char))
    memset(rseq[0], 0, blen * sizeof(unsigned char))
    memset(useq[0], 0, ulen * sizeof(unsigned char))

    # fill the bitmaps
    cdef int     kind
    cdef void*   data
    if isinstance(text, str):
        # make sure the unicode string is in canonical form,
        # --> won't be needed anymore in Python 3.12
        IF SYS_VERSION_INFO_MAJOR <= 3 and SYS_VERSION_INFO_MINOR < 12:
            PyUnicode_READY(text)
        # get the raw unicode buffer
        kind = PyUnicode_KIND(text)
        data = PyUnicode_DATA(text)
        fill_bitmap_from_unicode(kind, data, slen, seq, useq)
    elif slen > 0:
        fill_bitmap_from_buffer(text, seq, useq)

    # compute reverse complement and return
    sequence.rcom_seq(seq[0], rseq[0], useq[0], slen)
    return 0


cdef int fill_bitmap_from_unicode(
    const int kind,
    const void* data,
    const ssize_t length,
    bitmap_t* seq,
    bitmap_t* useq,
) except 1:
    cdef ssize_t i, j
    cdef Py_UCS4 letter
    with nogil:
        for i,j in enumerate(range(0, length*2, 2)):
            letter = PyUnicode_READ(kind, data, i)
            if letter == u'A' or letter == u'a':
                pass
            elif letter == u'T' or letter == u't':
                bitmap.set(seq[0], j)
                bitmap.set(seq[0], j+1)
            elif letter == u'G' or letter == u'g':
                bitmap.set(seq[0], j)
            elif letter == u'C' or letter == u'c':
                bitmap.set(seq[0], j+1)
            else:
                bitmap.set(seq[0],  j+1)
                bitmap.set(useq[0], i)
    return 0


cdef int fill_bitmap_from_buffer(
    const unsigned char[:] sequence,
    bitmap_t* seq,
    bitmap_t* useq,
) except 1:
    cdef ssize_t i, j
    cdef unsigned char letter
    with nogil:
        for i,j in enumerate(range(0, sequence.shape[0]*2, 2)):
            letter = sequence[i]
            if letter == b'A' or letter == b'a':
                pass
            elif letter == b'T' or letter == b't':
                bitmap.set(seq[0], j)
                bitmap.set(seq[0], j+1)
            elif letter == b'G' or letter == b'g':
                bitmap.set(seq[0], j)
            elif letter == b'C' or letter == b'c':
                bitmap.set(seq[0], j+1)
            else:
                bitmap.set(seq[0],  j+1)
                bitmap.set(useq[0], i)
    return 0


# ----------------------------------------------------------------------------

cdef size_t count_genes(_node* nodes, int path) nogil:
    """Count the number of genes found in the node list.

    Adapted from the `add_genes` function in ``genes.c``.

    Arguments:
        nodes (_node*): An array of dynamic programming nodes.
        path (int): An index found by `dprog.dprog`.

    Returns:
        size_t: The number of genes that can be extracted from the nodes list.

    """
    cdef size_t ctr = 0

    if path == -1:
        return 0

    while nodes[path].traceb != -1:
        path = nodes[path].traceb

    while path != -1 and ctr < gene.MAX_GENES:
        if nodes[path].elim != 1:
          if nodes[path].strand == 1 and nodes[path].type == sequence.STOP:
              ctr += 1
          elif nodes[path].strand == -1 and nodes[path].type != sequence.STOP:
              ctr += 1
        path = nodes[path].tracef

    return ctr


cdef size_t count_nodes(
    bitmap_t seq,
    bitmap_t rseq,
    size_t slen,
    bint closed,
    _mask* mlist,
    int nm,
    _training* tinf
) nogil:
    """Count the number of nodes to be added for the given sequence.

    Adapted from the `add_nodes` function in ``nodes.c``.

    Arguments:
        seq (bitmap_t): The input sequence.
        rseq (bitmap_t): The reverse-complement of the input sequence.
        slen (size_t): The input sequence length.
        closed (bool): Whether or not the sequence has closed ends.
        mlist (_mask*): The sequence mask, to ignore certain regions.
        nm (int): The length of the sequence mask.
        tinf (_training*): The training info to use to detect START and
            STOP codons.

    Returns:
        size_t: The number of nodes that can be created from the sequence.

    """
    cdef size_t  i     = 0
    cdef size_t  nn    = 0
    cdef size_t  slmod = slen%3

    cdef bint[3]   saw_start
    cdef size_t[3] last
    cdef size_t[3] min_dist

    # If sequence is smaller than a codon, there is no nodes so
    # we can early return here
    if slen < 3:
        return 0

    # Forward strand nodes
    for i in range(3):
        last[(i+slmod)%3] = slen + i
        saw_start[i%3] = False;
        min_dist[i%3] = node.MIN_EDGE_GENE;
        if not closed:
            while last[(i+slmod)%3] + 3 > slen:
                last[(i+slmod)%3] -= 3

    for i in range(slen-3, -1, -1):
        if sequence.is_stop(seq, i, tinf):
            if saw_start[i%3]:
                nn += 1
            min_dist[i%3] = node.MIN_GENE;
            last[i%3] = i;
            saw_start[i%3] = False;
            continue;

        if (last[i%3] >= slen):
            continue

        if not node.cross_mask(i, last[i%3], mlist, nm):
            if (
                    sequence.is_start(seq, i, tinf)
                and (last[i%3] - i + 3) >= min_dist[i%3]
                and (sequence.is_atg(seq, i) or sequence.is_gtg(seq, i) or sequence.is_ttg(seq, i))
            ):
                saw_start[i%3] = True;
                nn += 1
            elif i <= 2 and not closed and (last[i%3] - i) > node.MIN_EDGE_GENE:
                saw_start[i%3] = True;
                nn += 1

    for i in range(3):
        if saw_start[i%3]:
            nn += 1

    # Reverse strand nodes
    for i in range(3):
        last[(i+slmod)%3] = slen + i;
        saw_start[i%3] = False;
        min_dist[i%3] = node.MIN_EDGE_GENE;
        if not closed:
            while last[(i+slmod)%3] + 3 > slen:
                last[(i+slmod)%3] -= 3;

    for i in range(slen-3, -1, -1):
        if sequence.is_stop(rseq, i, tinf):
            if saw_start[i%3]:
                nn += 1
            min_dist[i%3] = node.MIN_GENE;
            last[i%3] = i;
            saw_start[i%3] = 0;
            continue;

        if(last[i%3] >= slen):
            continue

        if not node.cross_mask(slen-last[i%3]-1, slen-i-1, mlist, nm):
            if (
                    sequence.is_start(rseq, i, tinf)
                and (last[i%3] - i + 3) >= min_dist[i%3]
                and (sequence.is_atg(rseq, i) or sequence.is_gtg(rseq, i) or sequence.is_ttg(rseq, i))
            ):
                saw_start[i%3] = 1;
                nn += 1
            elif i <= 2 and not closed and (last[i%3] - i) > node.MIN_EDGE_GENE:
                saw_start[i%3] = 1;
                nn += 1

    for i in range(3):
        if saw_start[i%3]:
            nn += 1

    return nn;


# ----------------------------------------------------------------------------

# Initializing the metagenomic bins is fast enough that we can afford to do it
# only once, when the module is imported; storing them in a global means that:
#   1. we don't need to copy them in the results
#   2. we don't have to worry about their lifetime within the results

cdef _metagenomic_bin META_BINS[NUM_META]
cdef size_t _i
for _i in range(NUM_META):
    memset(&META_BINS[_i], 0, sizeof(_metagenomic_bin))
    META_BINS[_i].tinf = <_training*> PyMem_Malloc(sizeof(_training))
    if not META_BINS[_i].tinf:
        raise MemoryError()
    memset(META_BINS[_i].tinf, 0, sizeof(_training))
initialize_metagenomic_bins(META_BINS)


# ----------------------------------------------------------------------------

cdef class TrainingInfo:

    cdef bint       owned
    cdef _training* raw

    def __dealloc__(self):
        if self.owned:
            PyMem_Free(self.raw)

    @property
    def translation_table(self):
        """`int`: The translation table used during training.
        """
        return self.raw[0].trans_table

    @translation_table.setter
    def translation_table(self, int table):
        if table not in _TRANSLATION_TABLES:
            raise ValueError(f"{table} is not a valid translation table index")
        self.raw[0].trans_table = table

    @property
    def gc(self):
        """`float`: The GC content of the training sequence.
        """
        return self.raw[0].gc

    @gc.setter
    def gc(self, double gc):
        self.raw[0].gc = gc

    @property
    def bias(self):
        """`tuple` of `float`: The GC frame bias for each of the 3 positions.
        """
        return tuple(self.raw[0].bias)

    @bias.setter
    def bias(self, object bias):
        self.raw[0].bias = bias

    @property
    def type_weights(self):
        """`tuple` of `float`: The weights for the ATG, GTG and TTG codons.
        """
        return tuple(self.raw[0].type_wt)

    @type_weights.setter
    def type_weights(self, object type_weights):
        self.raw[0].type_wt = type_weights

    @property
    def uses_sd(self):
        """`bool`: `True` if the sequence uses a Shine/Dalgarno motif.
        """
        return self.raw[0].uses_sd

    @uses_sd.setter
    def uses_sd(self, bint uses_sd):
        self.raw[0].uses_sd = uses_sd


# ----------------------------------------------------------------------------

cdef class Genes:
    """A collection of all the genes found by Prodigal in a single sequence.

    It implements all the methods of `collection.abc.Sequence`, so genes can
    be accessed individually using an index, or iterated upon in forward or
    reverse mode. Genes are sorted by their leftmost coordinate, independently
    of the strand.

    Attributes:
        training_info (`pyrodigal.TrainingInfo`): A reference to the training
            info these genes were obtained from.

    """
    # expose the training info
    cdef readonly TrainingInfo training_info
    # the list of nodes in the input sequence
    cdef _node* nodes
    cdef size_t nn
    # the array of genes in the input sequence
    cdef _gene* genes
    cdef size_t ng
    # the training information
    cdef int _translation_table
    # the sequence length and bitmaps
    cdef size_t slen
    cdef bitmap_t seq
    cdef bitmap_t rseq
    cdef bitmap_t useq

    def __dealloc__(self):
        PyMem_Free(self.nodes)
        PyMem_Free(self.genes)
        PyMem_Free(self.seq)
        PyMem_Free(self.rseq)
        PyMem_Free(self.useq)

    def __len__(self):
        return self.ng

    def __getitem__(self, ssize_t index):
        if index < 0:
            index += <ssize_t> self.ng
        if index >= <ssize_t> self.ng or index < 0:
            raise IndexError("list index out of range")
        return self._gene(<size_t> index)

    def __iter__(self):
        return (self._gene(i) for i in range(self.ng))

    def __reversed__(self):
        return (self._gene(self.ng-i) for i in range(1, self.ng+1))

    cdef Gene _gene(self, size_t index):
        return Gene.__new__(Gene, self, index)


# ----------------------------------------------------------------------------

cdef class Gene:
    """A single gene found by Prodigal within a DNA sequence.
    """

    # a reference to the training info
    cdef readonly TrainingInfo training_info
    # a hard reference to the Genes instance that created this object
    # to avoid the data referenced by other pointers to be deallocated.
    cdef Genes genes
    # A reference to the nodes array and to the genes
    cdef _node* nodes
    cdef _gene* gene
    # A reference to the input sequence
    cdef size_t slen
    cdef bitmap_t* seq
    cdef bitmap_t* rseq
    cdef bitmap_t* useq
    # The translation table
    cdef int _translation_table

    def __cinit__(self, Genes genes, size_t index):
        if index > genes.ng:
            raise IndexError(index)
        self.genes = genes
        self.nodes = genes.nodes
        self.gene = &genes.genes[index]
        self.slen = genes.slen
        self.seq = &genes.seq
        self.useq = &genes.useq
        self.rseq = &genes.rseq
        self.training_info = genes.training_info
        self._translation_table = genes._translation_table

    @property
    def _data(self):
        return self.gene.gene_data.decode('ascii')

    @property
    def _score_data(self):
        return self.gene.score_data.decode('ascii')

    @property
    def begin(self):
        """`int`: The coordinate at which the gene begins.
        """
        return self.gene.begin

    @property
    def end(self):
        """`int`: The coordinate at which the gene ends.
        """
        return self.gene.end

    @property
    def strand(self):
        """`int`: *-1* if the gene is on the reverse strand, *+1* otherwise.
        """
        return self.nodes[self.gene.start_ndx].strand

    @property
    def partial_begin(self):
        """`bool`: whether the gene overlaps with the start of the sequence.
        """
        if self.strand == 1:
            return self.nodes[self.gene.start_ndx].edge == 1
        else:
            return self.nodes[self.gene.stop_ndx].edge == 1

    @property
    def partial_end(self):
        """`bool`: whether the gene overlaps with the end of the sequence.
        """
        if self.strand == 1:
            return self.nodes[self.gene.stop_ndx].edge == 1
        else:
            return self.nodes[self.gene.start_ndx].edge == 1

    @property
    def start_type(self):
        """`str`: The start codon of this gene.

        Can be one of ``ATG``, ``GTG`` or ``TTG``, or ``Edge`` if `Pyrodigal`
        has been initialized in open ends mode and the gene starts right at the
        beginning of the input sequence.
        """
        node = self.nodes[self.gene.start_ndx]
        start_type = 3 if node.edge else node.type
        return ["ATG", "GTG", "TTG" , "Edge"][start_type]

    @property
    def rbs_motif(self):
        """``str``, optional: The motif of the Ribosome Binding Site.

        Possible non-`None` values are ``GGA/GAG/AGG``, ``3Base/5BMM``,
        ``4Base/6BMM``, ``AGxAG``, ``GGxGG``, ``AGGAG(G)/GGAGG``, ``AGGA``,
        ``AGGA/GGAG/GAGG``, ``GGAG/GAGG``, ``AGGAG/GGAGG``, ``AGGAG``
        ``GGAGG`` or ``AGGAGG``.

        """
        cdef char* data = self.gene.gene_data
        cdef char* i = strstr(data, "rbs_motif")
        cdef char* j = <char*> memchr(i, b';', 30)
        cdef size_t length = j - i
        if i[10:length] == b"None":
            return None
        return i[10:length].decode("ascii")

    @property
    def rbs_spacer(self):
        """`str`, optional: The number of base pair between the RBS and the CDS.

        Possible non-`None` values are ``3-4bp``, ``5-10bp``, ``11-12bp`` or
        ``13-15bp``.

        """
        cdef char* data = self.gene.gene_data
        cdef char* i = strstr(data, "rbs_spacer")
        cdef char* j = <char*> memchr(i, b';', 30)
        cdef size_t length = j - i
        if i[11:length] == b"None":
            return None
        return i[11:length].decode("ascii")

    @property
    def gc_cont(self):
        """`float`: The GC content of the gene (between *0* and *1*).
        """
        cdef char* data = self.gene.gene_data
        cdef char* i = strstr(data, "gc_cont")
        cdef char* j = <char*> memchr(i, b'\0', 30)
        cdef size_t length = j - i
        return float(i[8:length])

    @property
    def translation_table(self):
        """`int`: The translation table used to find the gene.
        """
        return self._translation_table

    @property
    def cscore(self):
        """`float`: The coding score for the start node, based on 6-mer usage.

        .. versionadded:: 0.5.1

        """
        assert self.gene != NULL
        assert self.nodes != NULL
        return self.nodes[self.gene.start_ndx].cscore

    @property
    def rscore(self):
        """`float`: The score for the RBS motif.

        .. versionadded:: 0.5.1

        """
        assert self.gene != NULL
        assert self.nodes != NULL
        return self.nodes[self.gene.start_ndx].rscore

    @property
    def sscore(self):
        """`float`: The score for the strength of the start codon.

        .. versionadded:: 0.5.1

        """
        assert self.gene != NULL
        assert self.nodes != NULL
        return self.nodes[self.gene.start_ndx].sscore

    @property
    def tscore(self):
        """`float`: The score for the codon kind (ATG/GTG/TTG).

        .. versionadded:: 0.5.1

        """
        assert self.gene != NULL
        assert self.nodes != NULL
        return self.nodes[self.gene.start_ndx].tscore

    @property
    def uscore(self):
        """`float`: The score for the upstream regions.

        .. versionadded:: 0.5.1

        """
        assert self.gene != NULL
        assert self.nodes != NULL
        return self.nodes[self.gene.start_ndx].uscore

    cpdef unicode translate(self, translation_table=None):
        """Translate the gene into a protein sequence.

        Arguments:
            translation_table (`int`, optional): An alternative translation table
                to use to translate the gene. Use ``None`` (the default) to
                translate using the translation table this gene was found with.

        Returns:
            `str`: The proteins sequence as a string using the right translation
            table and the standard single letter alphabet for proteins.

        Raises:
            `ValueError`: when ``translation_table`` is not a valid number.

        """

        cdef size_t         nucl_length
        cdef size_t         prot_length
        cdef size_t         i
        cdef size_t         j
        cdef _mini_training mini_tinf
        cdef _training*     tinf
        cdef object         protein
        cdef int            kind
        cdef void*          data
        cdef Py_UCS4        aa
        cdef size_t         slen        = self.slen
        cdef bitmap_t       useq        = self.useq[0]
        cdef int            edge        = self.nodes[self.gene.start_ndx].edge
        cdef int            strand      = self.nodes[self.gene.start_ndx].strand
        cdef bitmap_t       seq
        cdef size_t         begin
        cdef size_t         end
        cdef size_t         unk

        # HACK: support changing the translation table (without allocating a
        #       new a training info structure) by manipulating where the
        #       table would be read from in the fields of the struct
        if translation_table is None:
            tinf = self.training_info.raw
        else:
            if translation_table not in _TRANSLATION_TABLES:
              raise ValueError(f"{translation_table} is not a valid translation table index")
            mini_tinf.trans_table = translation_table
            tinf = <_training*> &mini_tinf
            assert tinf.trans_table == translation_table

        # compute the right length to hold the protein
        nucl_length = (<size_t> self.gene.end) - (<size_t> self.gene.begin)
        prot_length = nucl_length//3 + (nucl_length%3 != 0)
        # create an empty protein string that we can write to
        # with the appropriate functions
        protein = PyUnicode_New(prot_length, 0x7F)
        kind    = PyUnicode_KIND(protein)
        data    = PyUnicode_DATA(protein)

        # compute the offsets in the sequence bitmaps:
        # - begin is the coordinates of the first nucleotide in the gene
        # - unk is the coordinate of the first nucleotide in the useq bitmap
        if strand == 1:
            begin = self.gene.begin
            end = self.gene.end
            seq = self.seq[0]
            unk = begin
        else:
            begin = self.slen + 1 - self.gene.end
            end = self.slen + 1 - self.gene.begin
            seq = self.rseq[0]
            unk = slen + 1 - begin

        # fill the sequence string, replacing residues with any unknown
        # nucleotide in the codon with an "X".
        with nogil:
            for i, j in enumerate(range(begin, end, 3)):
                if bitmap.test(useq, unk-1) or bitmap.test(useq, unk) or bitmap.test(useq, unk+1):
                    aa = "X"
                else:
                    aa = sequence.amino(seq, j-1, tinf, i==0 and edge==0)
                PyUnicode_WRITE(kind, data, i, aa)
                unk += 3 * strand

        # return the string containing the protein sequence
        return protein


# ----------------------------------------------------------------------------

cdef class Pyrodigal:
    """An efficient ORF finder for genomes, progenomes and metagenomes.

    Attributes:
        meta (`bool`): Whether or not this object is configured to
            find genes using the metagenomic bins or manually created
            training infos.
        closed (`bool`): Whether or not proteins can run off edges when
            finding genes in a sequence.
        training_info (`~pyrodigal.TrainingInfo`): The object storing the
            training information, or `None` if the object is in metagenomic
            mode.

    """
    #
    cdef readonly bint   closed
    cdef readonly object lock
    cdef readonly bint   meta
    cdef readonly size_t _num_seq

    #
    cdef size_t nn
    cdef _node* nodes
    cdef size_t max_nodes

    #
    cdef size_t ng
    cdef _gene* genes
    cdef size_t max_genes

    #
    cdef public TrainingInfo training_info

    def __init__(self, meta=False, closed=False):
        """Instantiate and configure a new ORF finder.

        Arguments:
            meta (`bool`): Set to `True` to run in metagenomic mode, using a
                pre-trained profiles for better results with metagenomic or
                progenomic inputs. Defaults to `False`.
            closed (`bool`): Set to `True` to consider sequences ends 'closed',
                which prevents proteins from running off edges. Defaults to
                `False`.

        """
        self.meta = meta
        self.closed = closed
        self.lock = threading.Lock()

    def __cinit__(self):
        self._num_seq = 1
        # node array, uninitialized on object creation to reduce memory usage
        self.max_nodes = 0
        self.nn = 0
        self.nodes = NULL
        # gene array, uninitialized on object creation to reduce memory usage
        self.max_genes = 0
        self.ng = 0
        self.genes = NULL

    def __dealloc__(self):
        PyMem_Free(self.nodes)
        PyMem_Free(self.genes)

    cpdef Genes find_genes(self, object sequence):
        """find_genes(self, sequence )\n--

        Find all the genes in the input DNA sequence.

        Arguments:
            sequence (`str` or buffer): The nucleotide sequence to use,
                either as a string of nucleotides, or as an object implementing
                the buffer protocol. Letters not corresponding to an usual
                nucleotide (not any of "ATGC") will be ignored.

        Returns:
            `Genes`: A collection of all the genes found in the input.

        Raises:
            `MemoryError`: When allocation of an internal buffers fails.
            `RuntimeError`: On calling this method without `train` in *single* mode.
            `TypeError`: When ``sequence`` does not implement the buffer protocol.

        """
        if not self.meta and self.training_info is None:
            raise RuntimeError("cannot find genes without having trained in single mode")

        cdef size_t slen = len(sequence)
        cdef bitmap_t seq = NULL
        cdef bitmap_t rseq = NULL
        cdef bitmap_t useq = NULL
        sequence_to_bitmap(sequence, &seq, &rseq, &useq)

        with self.lock:
            if self.meta:
                return self._find_genes_meta(slen, seq, useq, rseq)
            else:
                return self._find_genes_single(slen, seq, useq, rseq)

    cdef void _reallocate_genes(self, size_t new_genes) nogil:
        cdef size_t new_size = MIN_GENES if self.genes == NULL else self.max_genes
        while new_size < new_genes:
            new_size *= 2
        with gil:
            self.genes = <_gene*> PyMem_Realloc(self.genes, new_size*sizeof(_gene))
            if not self.genes:
                raise MemoryError()
            self.max_genes = new_size

    cdef void _reallocate_nodes(self, size_t new_nodes) nogil:
        cdef size_t new_size = MIN_NODES if self.nodes == NULL else self.max_nodes
        while new_size < new_nodes:
            new_size *= 2
        with gil:
            self.nodes = <_node*> PyMem_Realloc(self.nodes, new_size*sizeof(_node))
            if not self.nodes:
                raise MemoryError()
            self.max_nodes = new_size

    cdef Genes _find_genes_meta(self, size_t slen, bitmap_t seq, bitmap_t useq, bitmap_t rseq):
        cdef size_t i
        cdef size_t gene_count
        cdef size_t nodes_count

        cdef size_t gc_count = 0
        cdef double gc, low, high
        cdef double max_score = -100
        cdef size_t max_phase = 0

        with nogil:
            # compute the GC% of the sequence
            for i in range(slen):
                gc_count += sequence.is_gc(seq, i) * (1 - bitmap.test(useq, i))
            gc = (<double> gc_count) / (<double> slen) if slen > 0 else 0.0

            # compute the min/max acceptable gc for the sequence to only
            # use appropriate metagenomic bins
            low = 0.88495*gc - 0.0102337
            high = 0.86596*gc + .1131991
            if low > 0.65:
                low = 0.65
            if high < 0.35:
                high = 0.35

            # check which of the metagenomic bins gets the best results
            for i in range(NUM_META):
                # recreate the node list if the translation table changed
                if i == 0 or META_BINS[i].tinf.trans_table != META_BINS[i-1].tinf.trans_table:
                    # count the number of nodes to be added, reallocate if needed
                    nodes_count = count_nodes(seq, rseq, slen, self.closed, NULL, 0, META_BINS[i].tinf)
                    if nodes_count > self.max_nodes:
                        self._reallocate_nodes(nodes_count)
                    # add the dynamic programming nodes
                    memset(self.nodes, 0, self.nn*sizeof(_node))
                    self.nn = node.add_nodes(seq, rseq, slen, self.nodes, self.closed, NULL, 0, META_BINS[i].tinf)
                    qsort(self.nodes, self.nn, sizeof(_node), node.compare_nodes)

                # check the GC% is compatible with the current bin
                if META_BINS[i].tinf.gc < low or META_BINS[i].tinf.gc > high:
                    continue

                # compute the score for the current metagenomic bin
                node.reset_node_scores(self.nodes, self.nn)
                node.score_nodes(seq, rseq, slen, self.nodes, self.nn, META_BINS[i].tinf, self.closed, True)
                node.record_overlapping_starts(self.nodes, self.nn, META_BINS[i].tinf, 1)
                ipath = dprog.dprog(self.nodes, self.nn, META_BINS[i].tinf, 1)

                # update if the current bin gave a better score
                if self.nn > 0 and self.nodes[ipath].score > max_score:
                    max_phase = i
                    max_score = self.nodes[ipath].score
                    dprog.eliminate_bad_genes(self.nodes, ipath, META_BINS[i].tinf)
                    # reallocate memory for the nodes if this is the largest amount
                    # of genes found so far
                    gene_count = count_genes(self.nodes, ipath)
                    if gene_count > self.max_genes:
                        self._reallocate_genes(gene_count)
                    # extract the genes from the dynamic programming array
                    self.ng = gene.add_genes(self.genes, self.nodes, ipath)
                    gene.tweak_final_starts(self.genes, self.ng, self.nodes, self.nn, META_BINS[i].tinf)
                    gene.record_gene_data(self.genes, self.ng, self.nodes, META_BINS[i].tinf, self._num_seq)

            # recover the nodes corresponding to the best run
            memset(self.nodes, 0, self.nn*sizeof(_node))
            self.nn = node.add_nodes(seq, rseq, slen, self.nodes, self.closed, NULL, 0, META_BINS[max_phase].tinf)
            qsort(self.nodes, self.nn, sizeof(_node), node.compare_nodes)
            node.score_nodes(seq, rseq, slen, self.nodes, self.nn, META_BINS[max_phase].tinf, self.closed, True)

        # make a `Genes` instance to store the results
        cdef Genes genes = Genes.__new__(Genes)
        genes._translation_table = META_BINS[max_phase].tinf.trans_table
        # expose the metagenomic training info
        genes.training_info = TrainingInfo.__new__(TrainingInfo)
        genes.training_info.owned = False
        genes.training_info.raw = META_BINS[max_phase].tinf
        # copy nodes
        genes.nn = self.nn
        genes.nodes = <_node*> PyMem_Malloc(self.nn*sizeof(_node))
        if not genes.nodes: raise MemoryError()
        memcpy(genes.nodes, self.nodes, self.nn*sizeof(_node))
        # copy genes
        genes.ng = self.ng
        genes.genes = <_gene*> PyMem_Malloc(self.ng*sizeof(_gene))
        if not genes.genes: raise MemoryError()
        memcpy(genes.genes, self.genes, self.ng*sizeof(_gene))
        # take ownership of bitmaps
        genes.slen = slen
        genes.seq = seq
        genes.rseq = rseq
        genes.useq = useq
        # free resources
        memset(self.nodes, 0, self.nn*sizeof(_node))
        memset(self.genes, 0, self.ng*sizeof(_gene))
        self.ng = self.nn = 0
        self._num_seq += 1
        # return the `Genes` instance
        return genes

    cdef Genes _find_genes_single(self, size_t slen, bitmap_t seq, bitmap_t useq, bitmap_t rseq):

        cdef int        ipath
        cdef size_t     nodes_count
        cdef size_t     gene_count
        cdef _training* tinf        = self.training_info.raw

        with nogil:
            # reallocate memory for the nodes if this is the biggest sequence
            # processed by this object so far
            nodes_count = count_nodes(seq, rseq, slen, self.closed, NULL, 0, tinf)
            if nodes_count > self.max_nodes:
                self._reallocate_nodes(nodes_count)

            # find all the potential starts and stops, and sort them
            memset(self.nodes, 0, self.nn*sizeof(_node))
            self.nn = node.add_nodes(seq, rseq, slen, self.nodes, self.closed, NULL, 0, tinf)
            qsort(self.nodes, self.nn, sizeof(_node), node.compare_nodes)

            # second dynamic programming, using the dicodon statistics as the scoring
            # function
            node.reset_node_scores(self.nodes, self.nn)
            node.score_nodes(seq, rseq, slen, self.nodes, self.nn, tinf, self.closed, False)
            node.record_overlapping_starts(self.nodes, self.nn, tinf, True)
            ipath = dprog.dprog(self.nodes, self.nn, tinf, True)

            if self.nn > 0:
                dprog.eliminate_bad_genes(self.nodes, ipath, tinf)

            # reallocate memory for the nodes if this is the largest amount
            # of genes found so far
            gene_count = count_genes(self.nodes, ipath)
            if gene_count > self.max_genes:
                self._reallocate_genes(gene_count)

            # extract the genes from the dynamic programming array
            self.ng = gene.add_genes(self.genes, self.nodes, ipath)
            gene.tweak_final_starts(self.genes, self.ng, self.nodes, self.nn, tinf)
            gene.record_gene_data(self.genes, self.ng, self.nodes, tinf, self._num_seq)

        # make a `Genes` instance to store the results
        cdef Genes genes = Genes.__new__(Genes)
        genes.training_info = self.training_info
        genes._translation_table = self.training_info.translation_table
        # copy nodes
        genes.nn = self.nn
        genes.nodes = <_node*> PyMem_Malloc(self.nn*sizeof(_node))
        if not genes.nodes: raise MemoryError()
        memcpy(genes.nodes, self.nodes, self.nn*sizeof(_node))
        # copy genes
        genes.ng = self.ng
        genes.genes = <_gene*> PyMem_Malloc(self.ng*sizeof(_gene))
        if not genes.genes: raise MemoryError()
        memcpy(genes.genes, self.genes, self.ng*sizeof(_gene))
        # take ownership of bitmaps
        genes.slen = slen
        genes.seq = seq
        genes.rseq = rseq
        genes.useq = useq
        # free resources
        memset(self.nodes, 0, self.nn*sizeof(_node))
        memset(self.genes, 0, self.ng*sizeof(_gene))
        self.ng = self.nn = 0
        self._num_seq += 1

        #
        return genes

    cpdef object train(self, object sequence, bint force_nonsd=False, double st_wt=4.35, int translation_table=11):
        """train(self, sequence, force_nonsd=False, st_wt=4.35, translation_table=11)\n--

        Search optimal parameters for the ORF finder using a training sequence.

        Arguments:
            sequence (`str` or buffer): The nucleotide sequence to use, either
                as a string of nucleotides, or as an object implementing the
                buffer protocol.
            force_nonsd (`bool`, optional): Set to ``True`` to bypass the heuristic
                algorithm that tries to determine if the organism the training
                sequence belongs to uses a Shine-Dalgarno motif or not.
            st_wt (`float`, optional): The start score weight to use. The default
                value has been manually selected by the PRODIGAL authors as an
                appropriate value for 99% of genomes.
            translation_table (`int`, optional): The translation table to use.

        Raises:
            `MemoryError`: When allocation of an internal buffers fails.
            `RuntimeError`: When calling this method while in *metagenomic* mode.
            `TypeError`: When ``sequence`` does not implement the buffer protocol.
            `ValueError`: When ``translation_table`` is not a valid number.

        """
        if self.meta:
            raise RuntimeError("cannot use training sequence in metagenomic mode")
        if translation_table not in _TRANSLATION_TABLES:
            raise ValueError(f"{translation_table} is not a valid translation table index")

        # check we have enough nucleotides to train
        cdef size_t slen = len(sequence)
        if slen < MIN_SINGLE_GENOME:
            raise ValueError(
              f"sequence must be at least {MIN_SINGLE_GENOME} characters ({slen} found)"
            )
        elif slen < IDEAL_SINGLE_GENOME:
            warnings.warn(
              f"sequence should be at least {IDEAL_SINGLE_GENOME} characters ({slen} found)"
            )

        # convert sequence to bitmap for dynamic programming
        cdef bitmap_t seq = NULL
        cdef bitmap_t rseq = NULL
        cdef bitmap_t useq = NULL
        sequence_to_bitmap(sequence, &seq, &rseq, &useq)

        # create the training structure and compute GC content
        cdef _training* tinf = <_training*> PyMem_Malloc(sizeof(_training))
        memset(tinf, 0, sizeof(_training));
        tinf.gc = gc_content(seq, 0, slen-1)
        tinf.st_wt = st_wt
        tinf.trans_table = translation_table

        cdef int*   gc_frame;
        cdef int    ipath;
        cdef size_t nodes_count
        with self.lock:
            with nogil:
                # reallocate memory for the nodes if this is the biggest sequence
                # processed by this object so far
                nodes_count = count_nodes(seq, rseq, slen, self.closed, NULL, 0, tinf)
                if nodes_count > self.max_nodes:
                    self._reallocate_nodes(nodes_count)

                # find all the potential starts and stops and sort them
                self.nn = node.add_nodes(seq, rseq, slen, self.nodes, self.closed, NULL, 0, tinf)
                qsort(self.nodes, self.nn, sizeof(_node), node.compare_nodes)

                # scan all the ORFs looking for a potential GC bias in a particular
                # codon position, in order to acquire a good initial set of genes
                gc_frame = calc_most_gc_frame(seq, slen)
                if not gc_frame:
                    raise MemoryError()
                node.record_gc_bias(gc_frame, self.nodes, self.nn, tinf)
                free(gc_frame)

                # do an initial dynamic programming routine with just the GC frame bias
                # used as a scoring function.
                node.record_overlapping_starts(self.nodes, self.nn, tinf, 0)
                ipath = dprog.dprog(self.nodes, self.nn, tinf, 0)

                # gather dicodon statistics for the training set
                node.calc_dicodon_gene(tinf, seq, rseq, slen, self.nodes, ipath)
                node.raw_coding_score(seq, rseq, slen, self.nodes, self.nn, tinf)

                # determine if this organism uses Shine-Dalgarno and score the node
                node.rbs_score(seq, rseq, slen, self.nodes, self.nn, tinf)
                node.train_starts_sd(seq, rseq, slen, self.nodes, self.nn, tinf)
                if force_nonsd:
                    tinf.uses_sd = False
                else:
                    node.determine_sd_usage(tinf)
                if not tinf.uses_sd:
                    node.train_starts_nonsd(seq, rseq, slen, self.nodes, self.nn, tinf)

            # reset internal buffers and free allocated memory
            PyMem_Free(seq)
            PyMem_Free(rseq)
            PyMem_Free(useq)
            memset(self.nodes, 0, self.nn*sizeof(_node))
            self.nn = 0

        # store the training information in a Python object so it can be
        # shared with reference counting in the later `find_genes` calls
        self.training_info = TrainingInfo.__new__(TrainingInfo)
        self.training_info.owned = True
        self.training_info.raw = tinf

        return None
