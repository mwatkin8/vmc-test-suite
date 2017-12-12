from ctypes import *
import pandas as pd

vmc_lib = cdll.LoadLibrary('./govcf-vmc.so')
print("Generating the VMC unique IDs")

vmc_lib.Transform()

with open("go.vcf", "r") as go:
    go_rows = ""
    for line in go:
        go_rows += line
    with open("go.vcf", "r") as go:
        with open("../static/uploads/test.vcf") as transform:
            go_df =  pd.read_table(go)
            header = ""
            cols = ""
            for line in transform:
                if line[1] == "#":
                    header += line
                elif line[0] == "#":
                    cols += line
                    header += '''##INFO=<ID=VMCGSID,Number=1,Type=String,Description="VMC Sequence identifier">\n''' + '''##INFO=<ID=VMCGLID,Number=1,Type=String,Description="VMC Location identifier">\n''' + '''##INFO=<ID=VMCGAID,Number=1,Type=String,Description="VMC Allele identifier">\n'''

            with open("../static/uploads/out.vcf", "w") as out:
                out.write(header + cols + go_rows)
