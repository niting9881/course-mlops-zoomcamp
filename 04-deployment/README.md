# FAQ: ML Model Deployment

---

## 1. What are the main modes of ML model deployment?

There are two primary modes for deploying ML models:

- **Batch Deployment:**  
  Models are run on batches of data at scheduled intervals (e.g., hourly, daily). Predictions are stored for later use.
- **Online Deployment:**  
  Models are served in real-time, responding to requests as they arrive.

---

## 2. What is Batch Model Deployment?

- **How it works:**  
  Data is collected over a period, and predictions are made for the entire batch at once.
- **Use cases:**  
  - Generating daily recommendations
  - Fraud detection on end-of-day transactions
  - Periodic risk scoring

- **Model Serving in Batch Mode:**  
  - The model is loaded in a script or job (e.g., Python script, Airflow DAG).
  - The script processes input files (CSV, Parquet, etc.), makes predictions, and writes results to storage (database, file, etc.).
  - No web server is required.
  - Example:  
    ```python
    # Load model
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)
    # Read batch data, make predictions, save results
    ```

---

## 3. What is Online Model Deployment?

- **How it works:**  
  The model is always available to respond to prediction requests in real-time.
- **Use cases:**  
  - Real-time product recommendations
  - Chatbots
  - Fraud detection at transaction time

### Online Deployment: Web Services vs. Streaming

| Feature         | Web Services (REST/gRPC)         | Streaming (Kinesis/SQS/Lambda)      |
|-----------------|----------------------------------|-------------------------------------|
| **Request Type**| Synchronous (request/response)   | Asynchronous (event-driven)         |
| **Latency**     | Low (ms to sec)                  | Low to moderate (depends on pipeline)|
| **Scalability** | Scales with web server           | Scales with stream consumers        |
| **Examples**    | Flask, FastAPI, MLflow serving   | AWS Kinesis, SQS, Lambda            |
| **Use Case**    | Real-time APIs                   | High-throughput, event-driven tasks |

---

## 4. How do I serve a model as a web service?

- **Using Flask/FastAPI:**  
  - Wrap your model in an API endpoint.
  - Deploy as a web service (Docker, cloud, etc.).
  - Example:
    ```python
    from flask import Flask, request, jsonify
    app = Flask(__name__)
    @app.route('/predict', methods=['POST'])
    def predict():
        # Load model, process input, return prediction
        ...
    ```

- **Using MLflow:**  
  - Use `mlflow models serve` to deploy a model as a REST API.

---

## 5. How do I serve a model in batch mode?

- **Typical workflow:**
  1. Schedule a job (cron, Airflow, etc.) to run your prediction script.
  2. The script loads the model, processes a batch of data, and writes predictions to storage.
  3. No web server or API is needed.

---

## 6. How do I deploy a streaming model using Kinesis, SQS, and Lambda?

- **AWS Kinesis:**  
  - Ingests streaming data (e.g., clickstreams, logs).
  - A consumer application (or Lambda) reads records, loads the model, and makes predictions in near real-time.

- **AWS SQS (Simple Queue Service):**  
  - Messages (data points) are sent to a queue.
  - A worker or Lambda function polls the queue, processes messages, and makes predictions.

- **AWS Lambda:**  
  - Serverless compute service.
  - Can be triggered by Kinesis or SQS events.
  - Loads the model (ideally from a fast-access location like S3 or Lambda layer), processes the event, and returns the prediction.

- **Example Streaming Architecture:**
  ```
  [Producer] --> [Kinesis Stream] --> [Lambda Function] --> [Prediction Output]
  [Producer] --> [SQS Queue] --> [Lambda Function] --> [Prediction Output]
  ```

---

## 7. When should I use batch vs. online vs. streaming deployment?

- **Batch:**  
  - When predictions are not needed instantly.
  - When processing large volumes of data at once is more efficient.

- **Online (Web Service):**  
  - When you need real-time predictions for user-facing applications.

- **Streaming:**  
  - When you have continuous data flows and need near real-time predictions at scale.

---

## 8. Can I combine these approaches?

Yes! Many production systems use a hybrid approach:
- Batch for periodic scoring and analytics.
- Online for real-time user interactions.
- Streaming for high-throughput, event-driven use cases.

---

## 9. Further Reading

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [AWS Kinesis](https://aws.amazon.com/kinesis/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [AWS SQS](https://aws.amazon.com/sqs/)
- [Flask](https://flask.palletsprojects.com/)
- [FastAPI](https://fastapi.tiangolo.com/)

---
