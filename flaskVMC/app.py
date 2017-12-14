# import the Flask class from the flask module
from flask import Flask, session, flash, render_template, request, redirect, url_for, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField
import os
import transform

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['vcf'])

# create the application object
app = Flask(__name__, static_folder='static')
app.secret_key = "12345"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# use decorators to link the function to a url
def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
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
        in_file = "static/uploads/in.vcf"
        out_file = "static/uploads/out.vcf"

        if os.path.isfile(in_file):
            os.remove(in_file)
        if os.path.isfile(out_file):
            os.remove(out_file)

    return render_template('index.html')  # render a template

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
