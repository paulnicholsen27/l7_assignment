import os 

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "uploads"

@app.route('/')
def index():
    print("loaded")
    return render_template('index.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'file uploaded successfully'
    else:
        return "yay"
		
if __name__ == '__main__':
    app.run(debug = True)