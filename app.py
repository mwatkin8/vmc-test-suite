"""app.py initiates the flask webapp and renders the html contained in the
templates folder. It calls the transform module to generate and insert the
unique identifiers and feeds the output to the front-end web page
"""
import os
from flask import Flask, flash, render_template, \
    request, redirect, send_from_directory
import transform #our custom-made module

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['vcf'])

# create the application object
APP = Flask(__name__, static_folder='static')
APP.secret_key = "vmctestsuite"
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_filename(filename):
    """Makes sure the filename is """
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@APP.route('/', methods=['GET', 'POST'])
def home():
    with open("static/json/example.json") as f_in:
        file_content = f_in.read()
        json_example = file_content

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
            with open("static/uploads/" + file.filename) as f_in:
                file_content = f_in.read()
                vcf_in = file_content
                return render_template('index.html',vcf_in=vcf_in,json_example=json_example)

    return render_template('index.html',json_example=json_example)

@APP.route('/transformed_vcf', methods=['GET', 'POST'])
def display_transformed():
    with open("static/json/example.json") as f_in:
        file_content = f_in.read()
        json_example = file_content

    filename = os.listdir("static/uploads")[1]
    if len(os.listdir("static/uploads")) < 3:
        out_filename = "vmc_" + filename
        out_path = "static/uploads/" + out_filename
        transform.run(filename, out_filename)
        if os.path.isfile('static/uploads/' + out_filename):
            with open('static/uploads/' + filename) as f_in:
                file_content = f_in.read()
                vcf_in = file_content
            with open('static/uploads/' + out_filename) as f_out:
                file_content = f_out.read()
                transformed_vcf = file_content
    else:
        out_filename = os.listdir("static/uploads")[1]
        #print(out_filename)
        out_path = "static/uploads/" + out_filename
        with open('static/uploads/' + filename) as f_in:
            file_content = f_in.read()
            vcf_in = file_content
        with open('static/uploads/' + out_filename) as f_out:
            file_content = f_out.read()
            transformed_vcf = file_content
    return render_template('index.html', json_example=json_example, vcf_in=vcf_in, transformed_vcf=transformed_vcf, out=out_path)

# start the server with the 'run()' method
if __name__ == '__main__':
    APP.run(debug=True, host="0.0.0.0")
