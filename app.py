"""app.py initiates the flask webapp and renders the html contained in the
templates folder. It calls the transform module to generate and insert the
unique identifiers and feeds the output to the front-end web page
"""
import os
from flask import Flask, flash, render_template, \
    request, redirect, send_from_directory
import transform
import bundle
import re

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['vcf'])

# create the application object
APP = Flask(__name__, static_folder='static')
APP.secret_key = "vmctestsuite"
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_filename(filename):
    """Makes sure the filename is """
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_upload(filename):
    with open("static/uploads/" + filename) as f_in:
        return f_in.read()
        
def get_transform(filename):
    with open(filename) as f_out:
        return f_out.read()

def get_json_example():
    with open("static/example.json") as f_in:
        return f_in.read()
        
def get_json_bundle(filename):
    with open(filename) as f_in:
        return f_in.read()

def get_filename():
    return os.listdir("static/uploads")[1]

def get_out_paths():
    r = re.compile('.+.vcf')
    filename = list(filter(r.match, os.listdir("static/uploads")))[0]
    json = "static/downloads/" + filename.split(".")[0] + ".json"
    vcf = "static/downloads/vmc_" + filename
    return json,vcf
    
@APP.route('/', methods=['GET', 'POST'])
def home():
    json_example = get_json_example()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # Check for a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
            file.save(os.path.join(APP.config['UPLOAD_FOLDER'], file.filename))
            vcf_in = get_upload(file.filename)
            #Displays uploaded VCF with example JSON
            return render_template('index.html',vcf_in=vcf_in,json_example=json_example)
    #Displays example JSON
    return render_template('index.html',json_example=json_example)

@APP.route('/transformed_vcf', methods=['GET', 'POST'])
def display_transformed():
    json_example = get_json_example()
    filename = get_filename()
    json,vcf = get_out_paths()
    vcf_in = get_upload(filename)
    r = re.compile('.+.vcf')
    if filter(r.match, os.listdir("static/downloads")):
        transform.run(filename, vcf)
        transformed_vcf = get_transform(vcf)
    else:
        transformed_vcf = get_transform(vcf)

    #Displays uploaded VCF, transformed VCF, and JSON example
    return render_template('index.html', json_example=json_example, vcf_in=vcf_in, transformed_vcf=transformed_vcf, vcf_out=vcf)

@APP.route('/bundle', methods=['GET', 'POST'])
def display_bundle():
    json_example = get_json_example()
    filename = get_filename()
    json,vcf = get_out_paths()
    vcf_in = get_upload(filename)
    json_example = get_json_example()
    bundle.run(json)
    json_bundle = get_json_bundle(json)
    r = re.compile('.+.vcf')
    if filter(r.match, os.listdir("static/downloads")):
        transformed_vcf = get_transform(vcf)
        return render_template('index.html', json_example=json_example, vcf_in=vcf_in, transformed_vcf=transformed_vcf, json_bundle=json_bundle, vcf_out=vcf, json_out=json)
    else:
        return render_template('index.html', json_example=json_example, vcf_in=vcf_in, json_bundle=json_bundle, json_out=json)

    
# start the server with the 'run()' method
if __name__ == '__main__':
    APP.run(debug=True, host="0.0.0.0")
