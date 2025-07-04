Here's an updated and **very detailed `README.md`** that consolidates everything you've shown:

* Kafka-based streaming app
* Flask web interface
* ML models for `.exe` and URL malware detection
* Spark SQL backend
* Organized folder structure and training artifacts

---

# 🔐 Real-time Malware Detection Platform using Flask, Kafka, Spark & ML

> Developed by **Ayush Mishra**

A full-stack platform for **real-time detection of malware in `.exe` files and URLs**, integrated with **Apache Kafka** for streaming, **Spark SQL** for analytics, and **machine learning** models for robust prediction. The system is web-accessible using Flask and supports dashboards, SQL analytics, and model training.

---

## 🧩 Key Features

* 📤 **Upload EXE files** or 🔗 **submit URLs** to detect threats using trained models
* 💡 Live stream data into **Kafka topics** for asynchronous processing
* 🧪 Analyze datasets using **custom SQL queries** backed by Spark
* 📊 Redirect to interactive **Streamlit dashboards** for visual insights
* 📁 Model training and preprocessing logic organized into separate modules

---

## ⚙️ Tech Stack

| Layer             | Technology                                |
| ----------------- | ----------------------------------------- |
| **Frontend**      | HTML (Flask templates), Streamlit UI      |
| **Backend API**   | Flask, Python, Session, Routing           |
| **Streaming**     | Apache Kafka (localhost:9092)             |
| **Processing**    | `os.popen()`, subprocess (model triggers) |
| **SQL Analytics** | PySpark (Spark SQL on HDFS CSVs)          |
| **ML Models**     | XGBoost, CatBoost, Ensemble Model         |
| **Storage**       | HDFS for dataset persistence              |

---

## 📁 Folder Structure

```bash
.
├── app.py                    # Main Flask backend
├── flask_server.py           # Older/alternate Flask entrypoint
├── kafka_connect/
│   └── dstream.py            # Kafka message consumer logic
├── detection_models/
│   ├── exe/file_det.py       # EXE malware detection
│   └── url/url_main.py       # URL classification
├── model-training/           # ML models and training notebooks
│   ├── model-training.ipynb
│   ├── xgb_model.joblib
│   ├── stacked_model.pkl
│   ├── result.csv
│   └── trainLabels.csv
├── spark_sql.py              # PySpark SQL query execution
├── templates/                # HTML UI templates
├── uploads/                  # Uploaded files
├── static/                   # JS/CSS if needed
├── requirements.txt          # Python dependencies
├── start.sh / kafka.sh       # Startup scripts
```

---

## 🧪 Main Functionalities

### 📤 File Upload

* Upload `.exe` file via UI → Streamed to Kafka topic `file-upload-topic`
* File saved → Detected by `file_det.py` script → Prediction + features extracted
* Output shown in `result.html`

### 🌐 URL Detection

* Submit any URL
* URL processed by `url_main.py` and result is parsed & shown in `result_url.html`

### 📊 SQL Dashboard

* Submit a SQL query + dataset name (e.g., `Exe_file_csv`, `Url_csv`)
* Query is run on **HDFS-backed Spark DataFrames**
* HTML table rendered in the web app

### 📈 Streamlit Dashboard Redirection

* `/dashboard_dist` → localhost:8502
* `/dashboard_exe` → localhost:8503

---

## 💻 How to Run the App

### 🛠 1. Set up Kafka

```bash
# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka
bin/kafka-server-start.sh config/server.properties
```

### ⚙️ 2. Install Python Requirements

```bash
pip install -r requirements.txt
```

### ▶️ 3. Launch Flask Server

```bash
python app.py
# or
python flask_server.py
```

### 🔁 4. (Optional) Run Streamlit Dashboards

```bash
streamlit run dashboard/exe_dashboard.py --server.port 8502
streamlit run dashboard/url_dashboard.py --server.port 8503
```

### 🧪 5. Use SQL Analytics Interface

Upload CSV to HDFS under:

* `hdfs://mfg:9000/csv/2/Exe_file_csv`
* `hdfs://mfg:9000/csv/2/Url_csv`

Then submit SQL queries via UI (e.g., `SELECT * FROM df LIMIT 10`)

---

## 🧠 Machine Learning Models

| Model               | Type            | Purpose                        |
| ------------------- | --------------- | ------------------------------ |
| `xgb_model.joblib`  | XGBoost         | `.exe` malware classification  |
| `stacked_model.pkl` | Ensemble        | Ensemble of CatBoost & XGBoost |
| `url_main.py`       | Rule-based / ML | URL phishing/malware detection |

Training scripts and preprocessing notebooks are available in `model-training/`.

---

## 📝 Sample SQL Queries

```sql
-- View all features
SELECT * FROM df LIMIT 5;

-- Filter suspicious records
SELECT * FROM df WHERE SuspiciousAPI='True';

-- Average entropy by label
SELECT Label, AVG(Entropy) FROM df GROUP BY Label;
```

---

## 📷 Screenshots (Optional - For GitHub README)

| Upload Malware File   | Query Dashboard       | URL Malware Detection |
| --------------------- | --------------------- | --------------------- |
| ![](static/snap1.png) | ![](static/snap2.png) | ![](static/snap3.png) |

---

## 📌 TODO

* ✅ Add Kafka consumer in background to auto-process streamed files
* ✅ Move file processing to thread-safe subprocess
* ❌ Integrate real-time alert system (Twilio/Slack)
* ❌ Deploy on cloud (AWS/GCP) with Docker + Kafka Manager

---

## 🙋‍♂️ Author

Made with 💻 by [Ayush Mishra](https://github.com/Ayush-mishra-0-0)
Open to internships and collaboration opportunities! 🎯

---

## 📜 License

Licensed under the [MIT License](LICENSE)

---

Would you like this exported as a `.md` file? Or want me to generate one with badges and live project demo links?
