#!/usr/bin/python
import sys,argparse, requests, json, ast, sqlite3, re


def pull_variant_from_db():
    id_list = []
    with sqlite3.connect("../../data_dump/variants.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT ID FROM Variant")
        rows = cursor.fetchall()
        for row in rows:
            val = row[0]
            id_list.append(str(val))
    print(id_list)

def fetch_annotations(rs):

    return identifier

#Connect to the VEP annotation tool
def VEP(variant):
	server = "https://rest.ensembl.org"
	ext = "/vep/human/id/" + variant
	r = requests.get(server+ext, headers = {"Content-Type" : "application/json"})
	if not r.ok:
		r.raise_for_status()
		sys.exit()
	decoded = r.json()
	decoded = ast.literal_eval(repr(decoded))
	return json.dumps(decoded)

#Parse output from VEP json
def parse_VEP_json(vep_json):
    with open("data/output", "w") as out:
        j = json.loads(vep_json)
        out.write(str(j) + '\n\n')
        print ("json loaded")
        for field in j:
            if field["transcript_consequences"]:
                for consequence in field["transcript_consequences"]:
                    out.write(
						"Gene_symbol: " + consequence["gene_symbol"] +
						"\nBiotype: " + consequence["biotype"] +
						"\nConsequence_terms: " + consequence["consequence_terms"][0] +
						"\nImpact: " + consequence["impact"] + "\n\n")

def main(rs):
    #1 Parse the VCF
    #2 (once we have it up and running) query the database for that variant
    #3 If not there:
        #Digest it
        #Fetch variants for it
        #Add it to database
    #4 If it is there:
        #Ask which tools to see annotations
        #Ask which annotation fields to filter

    parse_VEP_json(VEP(rs))

#	parse_VEP_json(VEP(variant))

if __name__ == "__main__":
    with open("data/input", "r") as file_in:
        for rs in file_in:
            rs = rs.split()
            main(rs[0])
    """
	parser = argparse.ArgumentParser(
		description = "Gathers annotation information for a VMC standard variant")
	parser.add_argument( 'identifier',
		type = str,
		help = "Identifier should be the digest of a VMC standard variant"
		)
	args = parser.parse_args()
    """
