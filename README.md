
# VMC Test Suite

The Variant Modelling Collaboration (VMC) has developed both a standard representation format for DNA and RNA variants as well as an algorithm for generating unique identifiers based on that representation format. The notation, reference build used, and many other aspects of the new representation format are fed into this hash-bashed digest algorithm which will generate a unique identifier. If two variants are identical and are being correctly formatted to the new VMC standard, then the algorithm will generate matching identifiers. This is important because it allows for institution A to share variant information with institution B with institution B being able to compare their VMC identifiers with those provided from institution A. If they are identical then both institutions can be sure that they are talking about the exact same variant. This standard also opens the door for a variety of research and clinical tools which rely on consistent data representation.

This web tool is designed to take in a VCF file, add VMC unique identifiers for each variant, and return the transformed file to the user. This is an important first step in the realization of the goals of the VMC because it allows users to start utilizing VMC unique identifiers without needing to implement the somewhat complex algorithm needed to correctly generate the identifiers on their own.

## Installation

Python 3 and Go 1.9.2 should be installed and the following steps should be followed to run the suite:

1) Use  "<code>pip install -r requirements.txt</code>" to install system dependencies. Or activate the flask_venv virtual environment using  "<code>source activate flask_venv</code>".

2) Within the VMC directory, use  "<code>python app.py</code>" to activate the web server locally. Navigate your web browser to http://127.0.0.1:5000/ in order to view the web tool.

3) Once rendered, the tool requires a decomposed vcf file in order to transform it properly (per requirement by the VMC). A test file  "<code>HG00177_sml.vcf</code>" has been provided which is taken from the 1000 Genomes project.




### Compiling Go files if modified

The identifiers are generated using the govcf-vmc.go and vmc.go files. Changes to the govcf-vmc.go file require it to be re-compiled using:

<code>go build -buildmode=c-shared -o govcf-vmc.so govcf-vmc.go</code>
