from flask import Flask, flash, render_template, \
    request, redirect, send_from_directory
import transform, bundle, conversions, re, os

# create the application object
APP = Flask(__name__, static_folder='static')
APP.secret_key = "vmcsuite"
APP.config['UPLOAD_FOLDER'] = 'static/uploads'

def get_upload(filename):
    """Returns the uploaded VCF file as a string"""
    with open("static/uploads/" + filename) as f_in:
        return f_in.read()

def get_transform(filename):
    """Returns the transformed VCF file as a string"""
    with open(filename) as f_out:
        return f_out.read()

def get_json_example():
    """Returns the example JSON schema file as a string"""
    with open("static/example.json") as f_in:
        return f_in.read()

def get_json_bundle(filename):
    """Returns the transformed JSON file as a string"""
    with open(filename) as f_in:
        return f_in.read()

def get_filename():
    """Returns the name of the uploaded VCF file"""
    r = re.compile('.+.vcf')
    return list(filter(r.match, os.listdir("static/uploads")))[0]

def get_out_paths():
    """Creates paths to transformed VCF and JSON files ready for download"""
    r = re.compile('.+.vcf')
    filename = list(filter(r.match, os.listdir("static/uploads")))[0]
    json = "static/downloads/" + filename.split(".")[0] + ".json"
    vcf = "static/downloads/vmc_" + filename
    return json,vcf


@APP.route('/', methods=['GET', 'POST'])
def home():
    """
        Displays the example JSON schema, saves the uploaded VCF file to the uploads folder and then displays it as well.

    """
    json_example = get_json_example()
    if request.method == 'POST':
        #check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        file.save(os.path.join(APP.config['UPLOAD_FOLDER'], file.filename))
        vcf_in = get_upload(file.filename)
        #Displays uploaded VCF with example JSON
        return render_template('index.html',vcf_in=vcf_in,json_example=json_example)
    #Displays example JSON
    return render_template('index.html',json_example=json_example)


@APP.route('/transformed_vcf', methods=['GET', 'POST'])
def display_transformed():
    """
        Checks to see if the transformed VCF already exists in the downloads folder, generates it if not from transform.py, then displays it along with the
        example JSON schema and the original uploaded file. Also sends the filepath for downloading the transformed VCF file.
    """
    json_example = get_json_example()
    filename = get_filename()
    json,vcf = get_out_paths()
    vcf_in = get_upload(filename)
    #Check if transformed VCF exists in downloads folder
    r = re.compile('.+.vcf')
    if filter(r.match, os.listdir("static/downloads")):
        transform.run(filename, vcf)
        transformed_vcf = get_transform(vcf)
    else:
        transformed_vcf = get_transform(vcf)
    return render_template('index.html', json_example=json_example, vcf_in=vcf_in, transformed_vcf=transformed_vcf, vcf_outPath=vcf)


@APP.route('/bundle', methods=['GET', 'POST'])
def display_bundle():
    """
        Checks to see if the transformed JSON already exists in the downloads folder, generates it if not from bundle.py, then displays it along with the
        example JSON schema and the original uploaded file. Also sends the filepath for downloading the transformed JSON file.

    """
    json_example = get_json_example()
    filename = get_filename()
    json,vcf = get_out_paths()
    vcf_in = get_upload(filename)
    json_example = get_json_example()
    #Check if transformed JSON exists in downloads folder
    r = re.compile('.+.json')
    if filter(r.match, os.listdir("static/downloads")):
        json_bundle = get_json_bundle(json)
    else:
        bundle.run(filename, json)
        json_bundle = get_json_bundle(json)
    return render_template('index.html', json_example=json_example, vcf_in=vcf_in, json_bundle=json_bundle, json_outPath=json)


@APP.route('/hgvs', methods=['GET', 'POST'])
def hgvs_to_json():
    """
        Uses conversions.py to convert a HGVS string to a VMC JSON bundle and displays it along with the example JSON schema.

    """
    json_example = get_json_example()
    hgvs = request.form['hgvs_string']
    hgvs_json = conversions.from_hgvs(hgvs)
    return render_template('index.html', hgvs_json=hgvs_json, json_example=json_example)


# start the server with the 'run()' method
if __name__ == '__main__':
    APP.run(debug=True, host="0.0.0.0",port=8000)
