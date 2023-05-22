import os 
import base64
from io import BytesIO

from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from collections import Counter
from matplotlib.figure import Figure
import numpy as np 

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "uploads"

@app.route('/')
def index():
    print("loaded")
    return render_template('index.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        column_values = extract_data(path)
        freq_of_first_digits = count_by_first_digit(column_values)
        img_data = create_bar_graph(freq_of_first_digits)
        return render_template("show_graph.html", img_data=img_data), 200
    else:
        pass
    
def extract_data(path):
    with open(path, 'r') as f:
        line = f.readline().split("\t")
        if line:
            column_index = get_column_index(line)
        column_values = []
        while line:
            line = f.readline().split("\t")
            try:
                column_values.append(line[column_index])
                print(line[column_index])
            except IndexError:
                break
        return column_values

def get_column_index(line, label="7_2009"):
    i = line.index(label)
    if i > 0:
        return i
    else:
        raise IndexError("The requested column name could not be found in this row")
    
def count_by_first_digit(values):
    start_digits = [str(x)[0] for x in values]
    return Counter(start_digits)

def create_bar_graph(frequency_table):
        # Generate the figure **without using pyplot**.
    # fig = Figure()
    # ax = fig.subplots()
    # ax.plot([1, 2])
    # # Save it to a temporary buffer.
    # buf = BytesIO()
    # fig.savefig(buf, format="png")
    # # Embed the result in the html output.
    # data = base64.b64encode(buf.getbuffer()).decode("ascii")
    # return f"<img src='data:image/png;base64,{data}'/>"
    fig = Figure()
    plots = fig.subplots()
    labels, values = zip(*frequency_table.items())

    indexes = np.arange(len(labels))
    width = 1

    plots.bar(indexes, values, width)
    # plots.xticks(indexes + width * 0.5, labels)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

if __name__ == '__main__':
    app.run(debug=True)


# @app.route("/")
# def hello():
#     # Generate the figure **without using pyplot**.
#     fig = Figure()
#     ax = fig.subplots()
#     ax.plot([1, 2])
#     # Save it to a temporary buffer.
#     buf = BytesIO()
#     fig.savefig(buf, format="png")
#     # Embed the result in the html output.
#     data = base64.b64encode(buf.getbuffer()).decode("ascii")
#     return f"<img src='data:image/png;base64,{data}'/>"