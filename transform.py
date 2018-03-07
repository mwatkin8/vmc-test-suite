"""Transform module is a module which parses the variants in the VCF,
accesses the Go code needed to digest them into unique identifiers,
and writes the output into the out.vcf file.
"""
from ctypes import cdll
from collections import namedtuple

variant = namedtuple('variant', ['chrom', 'pos', 'id', 'ref', 'alt', 'qual', \
    'filter', 'info', 'format', 'other'])
class VCFVariant(variant):
    """The VCFVariant class represents a variant represented in a format widely used in
    the VCF. The other field refers to optional additional identifiers which may be used.
    """
    def __new__(cls, *args):
        return super().__new__(cls, args[0], args[1], args[2], args[3], args[4], \
            args[5], args[6], args[7], args[8], args[9])

    def __init__(self, *args):
        # YOUR CODE HERE
        self.__chrom = args[0]
        self.__pos = args[1]
        self.__varid = args[2]
        self.__ref = args[3]
        self.__alt = args[4]
        self.__qual = args[5]
        self.__filter = args[6]
        self.__info = args[7]
        self.__format = args[8]
        self.__other = args[9]

    def __str__(self):
        return self.__chrom + '\t' + self.__pos + '\t' + self.__varid + '\t' + self.__ref + '\t' \
            + self.__alt + '\t' + self.__qual + '\t' + self.__filter + '\t' + self.__info + '\t' \
            + self.__format + '\t' + self.__other

    @property
    def chrom(self):
        """Represents the chromosome number for that variant from the VCF"""
        return self.__chrom

    @property
    def pos(self):
        """Represents the position index for that variant from the VCF"""
        return self.__pos

    @property
    def varid(self):
        """Represents the rsID for that variant from the VCF"""
        return self.__varid

    @property
    def ref(self):
        """Represents the base from the reference genome at the same position as
        the variant from the VCF
        """
        return self.__ref

    @property
    def alt(self):
        """Represents alternate bases for that variant from the VCF"""
        return self.__alt

    @property
    def qual(self):
        """Represents the quality indicators for that variant from the VCF"""
        return self.__qual

    @property
    def filter(self):
        """Represents the filter used for that variant from the VCF"""
        return self.__filter

    @property
    def info(self):
        """Represents various identifiers for that variant from the VCF"""
        return self.__info

    @property
    def format(self):
        """Represents the format used for that variant from the VCF"""
        return self.__format

    @property
    def other(self):
        """Represents other fields for that variant from the VCF"""
        return self.__other


def parse_ids():
    """Returns a list of the new VMC identifiers from go.vcf."""
    id_list = []
    with open('go.vcf', 'r') as go_vcf:
        for line in go_vcf:
            id_list.append(line.strip())
    return id_list

def parse(filename):
    """Parses the header information from in.vcf and adds INFO entries to the
    meta-information section. Gets the new VMC identifiers from parseIDs()
    and adds them to the info fields of the variants via a vcfVariant object.
    Combines the header information with the updated variants.

    returns: the updated vcf file as a string
    """
    in_path = 'static/uploads/' + filename
    with open(in_path) as transform:
        header = ''
        cols = ''
        id_list = parse_ids()
        idx = 0
        variants = ""
        for line in transform:
            if line[1] == '#':
                header += line
            elif line[0] == '#':
                cols += line
                header += """##INFO=<ID=VMCGSID,Number=1,Type=String,Description="VMC Sequence identifier">\n""" \
                    + """##INFO=<ID=VMCGLID,Number=1,Type=String,Description="VMC Location identifier">\n""" \
                    + """##INFO=<ID=VMCGAID,Number=1,Type=String,Description="VMC Allele identifier">\n"""
            else:
                line_list = line.split('\t')
                var = VCFVariant(line_list[0], line_list[1], line_list[2], \
                    line_list[3], line_list[4], line_list[5], line_list[6], \
                    line_list[7] + id_list[idx], line_list[8], line_list[9])
                variants += var.__str__()
                idx += 1
        return header + cols + variants

def run(filename, out_filename):
    """Calls the Go code which creates the VMC identifiers.
    It then calls parse() to gather the updated file which it writes to out.vcf.
    """
    vmc_lib = cdll.LoadLibrary('./govcf-vmc.so')
    print('Generating the VMC unique IDs')
    vmc_lib.Transform(filename)
    #Write out to transformed file that the user can download
    out_path = 'static/uploads/' + out_filename
    with open(out_path, 'w') as out:
        out.write(parse(filename))
