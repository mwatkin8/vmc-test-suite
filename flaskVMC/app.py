# import the Flask class from the flask module
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['vcf'])

# create the application object
app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# use decorators to link the function to a url
@app.route('/')
def home():
    return "/transform = will render the VMC transform page"  # return a string

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/transform', methods=['GET', 'POST'])
def transform():
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
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('index.html')  # render a template

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
