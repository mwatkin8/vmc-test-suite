#Transform module

from ctypes import *
import pandas as pd
import sqlite3 as lite

def connectDB():
    db_name = "Digest_Sequence_ID.db"
    sql = """create table Sequence_Identifier
            (ID integer primary key autoincrement,
            Namespace text,
            Accession text,
            VMC_SeqID text,
            CURIE_ID text)"""
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        if cursor.fetchone() is None:
            cursor.execute(sql)
            db.commit()
        return(cursor, db)

def transform():
    vmc_lib = cdll.LoadLibrary('./govcf-vmc.so')
    print("Generating the VMC unique IDs")

    vmc_lib.Transform()

    with open("go.vcf", "r") as go:
        go_rows = ""
        for line in go:
            go_rows += line
        with open("go.vcf", "r") as go:
            with open("static/uploads/in.vcf") as transform:
                go_df =  pd.read_table(go)
                header = ""
                cols = ""
                for line in transform:
                    if line[1] == "#":
                        header += line
                    elif line[0] == "#":
                        cols += line
                        header += '''##INFO=<ID=VMCGSID,Number=1,Type=String,Description="VMC Sequence identifier">\n''' + '''##INFO=<ID=VMCGLID,Number=1,Type=String,Description="VMC Location identifier">\n''' + '''##INFO=<ID=VMCGAID,Number=1,Type=String,Description="VMC Allele identifier">\n'''

                #Write out to transformed file that the user can download
                with open("static/uploads/out.vcf", "w") as out:
                    out.write(header + cols + go_rows)

                #Write to the database to persist for future queries
                #cursor,db = connectDB()
