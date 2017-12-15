#Transform module

from ctypes import *
import pandas as pd
import sqlite3 as lite
from collections import namedtuple

variant = namedtuple("variant",['chrom','pos','id','ref', 'alt', 'qual', 'filter', 'info', 'format', 'other'])
class VCFVariant(variant):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9])
    def __init__(self, *args, name="null"):
        # YOUR CODE HERE
        self.chrom = args[0]
        self.pos = args[1]
        self.id = args[2]
        self.ref = args[3]
        self.alt = args[4]
        self.qual = args[5]
        self.filter = args[6]
        self.info = args[7]
        self.format = args[8]
        self.other = args[9]

    @property
    def chrom(self):
        return self.__chrom
    @chrom.setter
    def chrom(self,chrom):
        self.__chrom = chrom

    @property
    def pos(self):
        return self.__pos
    @pos.setter
    def pos(self,pos):
        self.__pos = pos

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self,id):
        self.__id = id

    @property
    def ref(self):
        return self.__ref
    @ref.setter
    def ref(self,ref):
        self.__ref= ref

    @property
    def alt(self):
        return self.__alt
    @alt.setter
    def alt(self,alt):
        self.__alt = alt

    @property
    def qual(self):
        return self.__qual
    @qual.setter
    def qual(self,qual):
        self.__qual = qual

    @property
    def filter(self):
        return self.__filter
    @filter.setter
    def filter(self,filter):
        self.__filter = filter

    @property
    def info(self):
        return self.__info
    @info.setter
    def info(self,info):
        self.__info = info

    @property
    def format(self):
        return self.__format
    @format.setter
    def format(self,format):
        self.__format = format

    @property
    def other(self):
        return self.__other
    @other.setter
    def other(self,other):
        self.__other = other

    def __str__(self):
        return self.chrom + '\t' + self.pos + '\t' + self.id + '\t' + self.ref + '\t' + self.alt + '\t' + self.qual + '\t' + self.filter + '\t' + self.info + '\t' + self.format + '\t' + self.other

def parseIDs():
    """Returns a list of the new VMC identifiers from go.vcf."""
    id_list= []
    with open("go.vcf", "r") as go:
        for line in go:
            id_list.append(line.strip())
    return id_list

def parse():
    """
    Parses the header information from in.vcf and adds INFO entries to the meta-information section.
    Gets the new VMC identifiers from parseIDs() and adds them to the info fields of the variants via a vcfVariant object.
    Combines the header information with the updated variants.

    returns: the updated vcf file as a string
    """
    with open("static/uploads/in.vcf") as transform:
        header = ""
        cols = ""
        id_list = parseIDs()
        idx = 0
        variants = ""
        for line in transform:
            if line[1] == "#":
                header += line
            elif line[0] == "#":
                cols += line
                header += '''##INFO=<ID=VMCGSID,Number=1,Type=String,Description="VMC Sequence identifier">\n''' + '''##INFO=<ID=VMCGLID,Number=1,Type=String,Description="VMC Location identifier">\n''' + '''##INFO=<ID=VMCGAID,Number=1,Type=String,Description="VMC Allele identifier">\n'''
            else:
                l = line.split('\t')
                variant = VCFVariant(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7] + id_list[idx], l[8], l[9])
                variants += variant.__str__()
                idx += 1
        return header + cols + variants

def transform():
    """
    Calls the Go code which creates the VMC identifiers.
    It then calls parse() to gather the updated file which it writes to out.vcf.
    """
    vmc_lib = cdll.LoadLibrary('./govcf-vmc.so')
    print("Generating the VMC unique IDs")

    vmc_lib.Transform()

    #Write out to transformed file that the user can download
    with open("static/uploads/out.vcf", "w") as out:
        out.write(parse())
