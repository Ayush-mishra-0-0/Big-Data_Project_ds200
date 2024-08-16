# Flask Web Application with Kafka Integration

This Flask web application handles file uploads, executes SQL queries, and performs malware detection with Kafka integration. The application includes multiple endpoints for diverse functionalities and utilizes Kafka for message streaming.

## Features

- **File Upload**: Upload files and send them to a Kafka topic.
- **Query Execution**: Execute SQL queries and process results.
- **Malware Detection**: Analyze executable files for malware.
- **URL Analysis**: Analyze URLs for security threats.
- **Dashboard Redirection**: Redirect to external dashboards for analytics.

## Prerequisites

- **Python 3.8+**: Ensure Python is installed.
- **Apache Kafka**: Should be running on `localhost:9092`.
- **Flask**: Web framework for Python.
- **Kafka Python Client**: Kafka client library for Python.
- **Flask-CORS**: To handle Cross-Origin Resource Sharing (CORS).

## Installation

1. **Clone the Repository:**
   ```bash
   git clone <your-repository-url>
   cd <your-repository-directory>
