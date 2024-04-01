from flask import Flask, request, render_template, jsonify, redirect, url_for
from kafka import KafkaProducer
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
producer = KafkaProducer(bootstrap_servers='localhost:9092')

@app.route('/')
def index():
    return render_template('index.html')

url='http://localhost:8502'
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return redirect(url)
    

@app.route('/xg_boost.html',methods=['GET'])
def xg_boost():
    return render_template('xg_boost.html')


@app.route('/Ensemble.html',methods=['GET'])
def Ensemble():
    return render_template('Ensemble.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    print('Upload request received')
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    file.save('uploads/' + file.filename)
    
    # Send the file to Kafka topic
    with open('uploads/' + file.filename, 'rb') as f:
        producer.send('file-upload-topic', f.read())
    
    return jsonify({'message': f'File "{file.filename}" uploaded successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True,port=5000)
