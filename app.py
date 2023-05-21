import os 

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from collections import Counter

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
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(path)
        extract_data(path)
        return 'file uploaded successfully'
    else:
        return "yay"
    
def extract_data(path):
    with open(path, 'r') as f:
        line = f.readline().split("\t")
        if line:
            column_index = get_column_index(line)
        print("file opened")
        column_values = []
        while line:
            line = f.readline().split("\t")
            # import ipdb; ipdb.set_trace()
            try:
                column_values.append(line[column_index])
                print(line[column_index])
            except IndexError:
                break
        print("Done")
        count_by_first_digit(column_values)

def get_column_index(line, label="7_2009"):
    i = line.index(label)
    if i > 0:
        return i
    else:
        raise IndexError("The requested column name could not be found in this row")
    
def count_by_first_digit(values):
    start_digits = [str(x)[0] for x in values]
    print(Counter(start_digits))


if __name__ == '__main__':
    app.run(debug=True)