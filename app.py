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
    """
    Renders index.html and waits for an upload request.
    If upload is initiated, save the file as in.vcf in the uploads folder.
    Clear the uploads folder if no post request is made.
    """
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
        # Check to see if it is a VCF file
        if allowed_filename(file.filename):
            if file:
                filename = "in.vcf"
                file.save(os.path.join(APP.config['UPLOAD_FOLDER'], filename))
                transform.run()
                #access out.VCF
                with open("static/uploads/out.vcf") as f_out:
                    file_content = f_out.read()
                    out = file_content
                    return render_template('index.html', object=out)
        else:
            flash('Can only process VCF files.')
    # Clear uploads folder
    else:
        in_file = "static/uploads/in.vcf"
        out_file = "static/uploads/out.vcf"

        if os.path.isfile(in_file):
            os.remove(in_file)
        if os.path.isfile(out_file):
            os.remove(out_file)

    return render_template('index.html')

@APP.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    """If a download is initiated, send out.vcf as an attachment"""
    return send_from_directory(APP.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# start the server with the 'run()' method
if __name__ == '__main__':
    APP.run(debug=True, host="0.0.0.0")
