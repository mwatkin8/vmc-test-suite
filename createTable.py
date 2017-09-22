import sqlite3

def create_table(db_name, sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()


if __name__ == "__main__":
    db_name = "variants.db"
    sql = """create table Variant
            (variantID integer,
            DIGEST text,
            CHROM integer,
            POS integer,
            ID text,
            REF text,
            ALT text,
            QUAL integer,
            FILTER text,
            primary key(variantID))"""

    create_table(db_name, sql)
