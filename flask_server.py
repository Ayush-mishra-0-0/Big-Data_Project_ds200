from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from kafka import KafkaProducer
from flask_cors import CORS
import os
import ast
from kafka_connect.dstream import process_result_data
from spark_sql import fun

app = Flask(__name__)
CORS(app)
producer = KafkaProducer(bootstrap_servers='localhost:9092')
app.secret_key = 'ayush' 

@app.route('/')
def index():
    return render_template('index.html')

url = 'http://localhost:8500'
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return redirect(url)

@app.route('/sql', methods=['GET'])
def sql():
    return render_template('sql.html')


@app.route('/run_query', methods=['POST'])
def run_query():
    if request.method == 'POST':
        query_text = request.form['queryText']
        print("Received query:", query_text)
        results = fun(query_text)
        # Assuming 'results' is a string or HTML content
        return results
    else:
        return jsonify({'error': 'Invalid request method'})
@app.route('/xg_boost.html', methods=['GET'])
def xg_boost():
    return render_template('xg_boost.html')

@app.route('/find_malware.html', methods=['GET'])
def find_malware():
    return render_template('find_malware.html')

@app.route('/find_malware_url.html', methods=['GET'])
def find_malware_url():
    return render_template('find_malware_url.html')

@app.route('/Ensemble.html', methods=['GET'])
def Ensemble():
    return render_template('Ensemble.html')

@app.route('/upload.html', methods=['POST'])
def upload_file():
    try:
        print('Upload request received')
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Ensure the uploads directory exists
        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        # Save the file
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Send the file to Kafka topic
        with open(file_path, 'rb') as f:
            producer.send('file-upload-topic', f.read())

        return jsonify({'message': f'File "{file.filename}" uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'exe'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/result', methods=['POST'])
def result():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    print(file.filename)
    # If the user does not select a file, the browser submits an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = file.filename
    parts = filename.split('.')

    if file and parts[1]=='exe':
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        cmd = f'python detection_models/exe/file_det.py {file_path}'
        result = os.popen(cmd).read()
        parts = result.split('{')
        first_line= parts[0]
        sub_parts = parts[-1].split('}')
        features_list= sub_parts[0]
        last_line= sub_parts[-1]
        # print(features_list)
        # print("hello")
        list1= '{'+features_list+'}'
        # print(list1)
        # print(type(list1))
        result_dict = ast.literal_eval(list1)
        # print(result_dict)
        # print(type(result_dict))
        process_result_data(result_dict)
        # print("hello")
        # print(result)
        session['result'] = result
        return render_template('result.html', header=first_line, features_list=features_list, last_line=last_line)
    else:
        return jsonify({'error': 'Invalid file type. Only .exe files are allowed.'}), 400
    

@app.route('/show_result', methods=['GET'])
def show_result():
    result = session.get('result', 'No result available')
    parts = result.split('{')
    first_line = parts[0]
    sub_parts = parts[-1].split('}')
    features_list = sub_parts[0]
    last_line = sub_parts[-1]
    last_line = last_line.split(']')[-1]
    return render_template('result.html', header=first_line, features_list=features_list, last_line=last_line)

if __name__ == '__main__':
    app.run(debug=True, port=5000)




# from flask import Flask, request, jsonify
# from kafka import KafkaProducer
# import os
# import subprocess

# app = Flask(__name__)
# producer = KafkaProducer(bootstrap_servers='localhost:9092')
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     try:
#         print('Upload request received')
#         if 'file' not in request.files:
#             return jsonify({'error': 'No file part'}), 400
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400

#         # Ensure the uploads directory exists
#         if not os.path.exists('uploads'):
#             os.makedirs('uploads')

#         # Save the file
#         file_path = os.path.join('uploads', file.filename)
#         file.save(file_path)

#         # Send the file to Kafka topic
#         with open(file_path, 'rb') as f:
#             producer.send('file-upload-topic', f.read())

#         # Trigger the processing script as a separate process
#         subprocess.Popen(["python", "kafka_code.py"])

#         return jsonify({'message': f'File "{file.filename}" uploaded successfully'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500