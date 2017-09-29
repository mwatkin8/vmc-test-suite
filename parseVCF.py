import sys, sqlite3, argparse

def insert_data(variant_list):
    sys.stdout.write('\rAdding variants to variants.db')
    sys.stdout.flush()
    with sqlite3.connect("../../data_dump/variants.db") as db:
        cursor = db.cursor()
        sql = "insert into Variant (DIGEST, CHROM, POS, ID, REF, ALT, QUAL, FILTER) values (?,?,?,?,?,?,?,?)"
        for values in variant_list:
            cursor.execute(sql, values)
        db.commit()
    sys.stdout.write('\rVariants added to variants.db            \n')
    sys.stdout.flush()

def parse_vcf(vcf):
    with open(vcf, "r") as in_vcf:
        variant_list = []
        count = 0
        for line in in_vcf:
            sys.stdout.write('\rParsing variant #' + str(count))
            sys.stdout.flush()
            if count == 1000000:
                break
            if line.startswith('#'):
                pass
            else:
                count += 1
                line = line.split()
                line.insert(0, "fd#" + str(count))
                line = line[:8]
                variant_list.append(tuple(line))

        sys.stdout.write('\rParsing finished              \n')
        sys.stdout.flush()
        return variant_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='designate a VCF file to insert variants from')
    args = parser.parse_args()

    insert_data(parse_vcf(args.file))
