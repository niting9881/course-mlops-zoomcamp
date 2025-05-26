# **1. What is MLflow?**

MLflow is an open-source platform for managing end-to-end machine learning workflows. It provides components for:

- Experiment tracking
- Reproducible runs
- Model registry
- Deployment support

**Official Docs:** [MLflow Documentation](https://mlflow.org/docs/latest/index.html)

# **2. MLflow Tracking Server**

To launch a local tracking server:

mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts

--backend-store-uri: Path for metadata storage (e.g., SQLite DB)

--default-artifact-root: Path for saving model artifacts


**Official Docs:** [MLflow Documentation](https://mlflow.org/docs/latest/tracking/)

# **3. Experiment Tracking in Code**

Set up your experiment tracking in your Python script:

import mlflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("experiment-name")

with mlflow.start_run():
    # log params, metrics, models here

**Official Docs:** [MLflow Documentation](https://mlflow.org/docs/latest/tracking/tracking-api#organizing-runs-in-experiments)

# **4. Logging Params, Metrics, and Models**

**Manual Logging:**

mlflow.log_param("param_name", value)
mlflow.log_metric("metric_name", value)
mlflow.sklearn.log_model(model, "model")

Autologging (for scikit-learn):

mlflow.sklearn.autolog()

**Official Docs:** [MLflow Documentation](https://mlflow.org/docs/latest/tracking/tracking-api#organizing-runs-in-experiments)


# **5. Hyperparameter Optimization (HPO)**

Using hyperopt to find the best model parameters:

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from hyperopt import STATUS_OK

def objective(params):
    with mlflow.start_run():
        rf = RandomForestRegressor(**params)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)
        rmse = mean_squared_error(y_val, y_pred, squared=False)

        mlflow.log_params(params)
        mlflow.log_metric("rmse", rmse)
        mlflow.sklearn.log_model(rf, "model")

        return {'loss': rmse, 'status': STATUS_OK}

**Official Docs:** [scikit-learn Documentation](https://scikit-learn.org/stable/modules/grid_search.html)

# **6. Querying and Registering Models**

**Connect to the Tracking Server:**

from mlflow.tracking import MlflowClient
client = MlflowClient(tracking_uri="http://127.0.0.1:5000")

Search Runs:

runs = client.search_runs(
    experiment_ids=[experiment_id],
    order_by=["metrics.rmse ASC"],
    max_results=5
)
best_run = runs[0]

Register the Best Model:

model_uri = f"runs:/{best_run.info.run_id}/model"
mlflow.register_model(model_uri, "random-forest-best-model")

**Official Docs:** [MLflow Documentation](https://mlflow.org/docs/latest/model-registry/))

# **7. Best Practices**

Launch the tracking server before logging experiments

Use clear experiment and model names

Log all relevant params and metrics

Use the model registry for versioning and stage promotion

# **8. Common Commands**

**Start full server:**

mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts

Start UI only:

mlflow ui

Set experiment (in code):

mlflow.set_experiment("experiment-name")

# **9. References & Links**

MLflow Docs -https://mlflow.org/docs/latest/index.html

Python API Reference - https://mlflow.org/docs/latest/python_api/index.html

MLflow GitHub https://github.com/mlflow/mlflow
