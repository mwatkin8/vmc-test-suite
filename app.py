# import the Flask class from the flask module
from flask import Flask, session, flash, render_template, request, redirect, url_for, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField
import os
import transform #our custom-made module

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['vcf'])

# create the application object
app = Flask(__name__, static_folder='static')
app.secret_key = "vmctestsuite"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowedFilename(filename):
    """Makes sure the filename is """
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
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
        if allowedFilename(file.filename):
            if file:
                filename = "in.vcf"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                transform.transform()
                #access out.VCF
                with open("static/uploads/out.vcf") as f:
                    file_content = f.read()
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

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def downloadFile(filename):
    """If a download is initiated, send out.vcf as an attachment"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
