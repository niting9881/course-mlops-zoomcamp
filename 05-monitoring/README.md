# Evidently AI: Comprehensive Overview

Evidently AI is an open-source Python library offering over 100 evaluation metrics, a declarative testing API, and a lightweight visual interface for analyzing results. Beyond the open-source library, the Evidently Cloud platform provides a comprehensive toolkit for AI testing and observability, including features like tracing, synthetic data generation, dataset management, evaluation orchestration, alerting, and a no-code interface. The main goal of Evidently is to assist teams in building and maintaining reliable, high-performing AI products, from predictive machine learning models to complex LLM-powered systems. It addresses the challenge that model quality can degrade over time, presenting monitoring as the solution to this degradation.

## Key Components and Functionalities

- **Evaluation Library:**
  - **Reports:** Objects that include the results of metric calculations, capable of being visualized as HTML or rendered as JSON/Python objects. Reports are essential for summarizing data, metrics, and test results. They can be configured to include various metrics related to data quality, integrity, data drift, and model performance. Examples of metrics that can be included are `ColumnDrift`, `DatasetDrift`, and `DatasetMissingValues`. Reports can be executed on a chosen cadence.
  - **Tests:** Used in conjunction with or instead of Reports to define evaluation conditions and help reduce alert fatigue. They enable quick verification of conditions, such as ensuring all input data columns are within a defined min-max range.
  - **Column Mapping:** An object that aids Evidently in correctly parsing data frames, particularly useful when standard column names (e.g., 'Target', 'Predictions') are not used or when categorical features are encoded as digits.

- **Workspaces and Projects:** Evidently uses workspaces as a storage base, which can be a local file system, to store reports and data. Projects are created within a workspace to organize and store reports, often including descriptions for clarity and easier understanding.

## Monitoring Approaches

Evidently supports multiple methods for setting up monitoring.

### 1. Batch Monitoring Jobs

- **Best for:** Batch ML pipelines, regression testing, and near real-time ML systems that do not require immediate quality evaluations.
- **How it works:**
  - **Build an evaluation pipeline:** Users create a pipeline within their infrastructure (e.g., Python script, cron job, or orchestrated with tools like Airflow or Prefect) to run monitoring jobs at regular intervals (e.g., hourly, daily) or when new data/labels become available.
  - **Run metric calculations:** The evaluation step in the pipeline utilizes the Evidently Python library's core evaluation API to compute Reports that summarize data, metrics, and test results.
  - **Store and visualize results:** The Report runs are stored in Evidently Cloud or a designated self-hosted workspace and then monitored on a Dashboard. Users can opt to store only metric summaries instead of raw inferences to protect privacy and avoid log duplication.
- **Benefits:** This approach decouples log storage from monitoring metrics, providing full control over the evaluation pipeline. It fits most ML evaluation scenarios, such as data drift detection and model quality checks, which often naturally operate in batches.

### 2. Tracing with Scheduled Evals

- **Best for:** LLM-powered applications.
- **How it works:**
  - **Instrument the application:** The Tracely library is used to capture all relevant application data, including inputs, outputs, and intermediate steps.
  - **Store raw data:** The Evidently Platform stores all raw data, creating a complete record of activity.
  - **Schedule evaluations:** Evaluations are configured to run automatically at scheduled times, generating Reports or running Tests directly on the Evidently Platform. Manual evaluations are also possible.
- **Benefits:** This approach simplifies data capture for complex traces, allows easy re-running of evaluations or adding new metrics due to raw data storage, and offers a no-code UI for management once instrumentation is set up.

## Monitoring Dashboard and Alerts

- **Dashboard:** A key component for tracking evaluation results over time. Dashboards can utilize pre-built Tabs or be customized with various monitoring Panels. Panels can display different metrics, such as inference counts or missing values, using various plot types like line, bar, or scatter.
- **Alerts:** Users can configure alerts based on Metric values or Test failures to receive notifications about potential issues.

## Integration with Other Tools

Evidently is designed to integrate into existing MLOps stacks:

- **PostgreSQL:** Evidently metrics can be logged into a PostgreSQL database.
- **Grafana:** This dashboarding tool can then use the PostgreSQL database as a data source to visualize Evidently metrics, such as prediction drift, number of drifted columns, and share of missing values. Grafana dashboards can be saved and reused.
- **Prefect:** Evidently monitoring jobs can be implemented as Prefect pipelines, where Python functions are transformed into tasks and the main script into a flow, aiding in the orchestration of the monitoring workflow.
- **Airflow:** Another common tool that can be used to orchestrate batch evaluation jobs.

## Machine Learning Monitoring Metrics

For effective ML model monitoring, several categories of metrics are essential:

- **Service Health:** Standard software service metrics like uptime, memory usage, and latency are crucial to ensure the service is functioning correctly.
- **Model Performance:** The specific metrics depend on the problem type (e.g., regression, classification, ranking). Examples include Mean Absolute Error (MAE) or Mean Absolute Percentage Error (MAPE) for regression; log loss, precision, or recall for classification; or ranking metrics. These often require ground truth data, which can be delayed.
- **Data Quality and Integrity:** Metrics that identify issues with input data, such as the share or amount of missing values, correct data types, and value ranges for columns.
- **Data Drift and Concept Drift:** These metrics compare the distributions of input data, model output, or target function against a reference dataset where the model performed well. They serve as early signals for potential problems. Data drift detection naturally works in batches.

Additional, more advanced metrics can include:

- **Quality Metrics by Segments:** For diverse audiences or objects, evaluating quality separately for different categories.
- **Model Bias and Fairness:** Important in sensitive domains like healthcare or finance.
- **Outliers:** Monitoring individual anomalous objects, especially when the cost of error is high.
- **Explanations:** For recommender systems, sharing information about how recommendations were generated to build user trust.
## Resources

- [Introduction](https://docs.evidentlyai.com/introduction)
- [Quickstart](https://docs.evidentlyai.com/quickstart_llm)
- [Installation](https://docs.evidentlyai.com/docs/setup/installation)
- [Monitoring](https://docs.evidentlyai.com/docs/platform/monitoring_overview)
- [Dashboard](https://docs.evidentlyai.com/docs/platform/dashboard_overview)