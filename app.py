from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get name from the form
        name = request.form['name']

        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']

        # If the user does not select a file, the browser submits an empty part without filename
        if file.filename == '':
            return 'No selected file'
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # You can save the name and filename in a database if needed
            # For simplicity, we're just returning the name and filename
            return f'Name: {name}, File saved as: {filename}'
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)