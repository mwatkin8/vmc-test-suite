import sqlite3

def drop_table(db_name, sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()


if __name__ == "__main__":
    db_name = "variants.db"
    sql = """drop table Variant"""

    drop_table(db_name, sql)
