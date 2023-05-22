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
    start_digit_frequency = Counter([str(x)[0] for x in values])
    start_digit_percentages = {int(i): round(start_digit_frequency[i] / len(values) * 100.0, 2) for i in start_digit_frequency}
    return start_digit_percentages

def create_bar_graph(frequency_table):
    fig = Figure()
    axes = fig.subplots()
    labels = [i for i in range(1,10)] # choosing to ignore zero
    values = [frequency_table[j] for j in labels]

    indexes = np.arange(len(labels))
    width = 0.3
    bottom = np.zeros(9)

    axes.set_title("Percentage of numbers beginning with given digit")
    axes.bar(indexes - 0.15, values, width)
    axes.bar(indexes + 0.15, get_benford_values(), width)
    axes.set_xticks(indexes, labels)
    axes.set_ylabel("Percentage")
    axes.set_xlabel("Leading digit")
    buf = BytesIO()
    axes.legend(["Dataset value", "Expected value"])
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

def get_benford_values():
    return [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)