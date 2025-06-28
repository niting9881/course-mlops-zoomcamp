# Study Notes & FAQ: Unit Testing, Integration Testing, and LocalStack for AWS Services

## Overview: Best Engineering Practices for Testing

This guide covers best engineering practices for testing, focusing on unit tests and integration tests for serverless machine learning services. The key concepts include:

- **Types of Tests:**  
  - **Unit Tests:** Test individual functions or small "units" of code. They should be fast, independent, and not rely on external services like S3. Pytest is a popular framework, but Python's built-in `assert` can also be used. Code is often refactored into modular components (e.g., classes in a `model.py` file) to facilitate unit testing. Mock objects can simulate model behavior without loading from S3.
  - **Integration Tests:** Ensure that different parts of the system work together. This often involves running the service in a Docker container, sending requests, and verifying responses. For serverless ML services, integration tests should cover interactions with AWS services like Kinesis or S3. LocalStack can be used to emulate AWS services locally, avoiding dependency on real AWS accounts or internet connectivity.
  - **End-to-End Tests:** Integration tests can also serve as end-to-end tests, verifying both the service's response and its ability to interact with external systems (e.g., writing to a Kinesis stream).

- **Testing Practices and Tools:**  
  - **Code Refactoring for Testability:** Extract core logic from AWS Lambda functions into separate modules and classes to make code more modular and easier to test. Avoid global variables that can cause import issues.
  - **Assertions and Detailed Comparisons:** Use `assert` statements for checks. For complex data structures, use [DeepDiff](https://github.com/seperman/deepdiff) to pinpoint differences, including floating-point tolerance.
  - **Automating Tests with Scripts:** Use shell scripts (e.g., `run.sh`) to automate building Docker images, orchestrating services with Docker Compose, running test scripts, and cleaning up containers.
  - **Configuring with Environment Variables:** Use environment variables (e.g., `MODEL_BUCKET`, `KINESIS_ENDPOINT_URL`) for flexible and adaptable test setups.
  - **Robust Scripting for CI/CD:** Ensure test scripts exit with the correct code to signal success or failure in CI/CD pipelines. Use `set -e` in bash or check error codes explicitly.
  - **Callbacks for Flexibility:** Use callback functions to make prediction handling modular and testable, allowing different behaviors for test and production runs.
  - **Makefiles for Unified Control:** Use Makefiles to manage and run all tests and code quality checks with a single command.

---

## 1. Overview of Software Testing Methodologies

### Unit Tests
- **Purpose:** Test functions or small pieces of code in isolation, ensuring correctness and behavior without external dependencies.
- **Scope:** Very limited, focusing on a single function or a small module.
- **Characteristics:** Fast to execute, help identify bugs early, and serve as documentation for the code.

### Integration Tests
- **Purpose:** Ensure that combined units or modules function together as expected, verifying interactions between components, including databases, APIs, or external services.
- **Scope:** Broader than unit tests, encompassing multiple components or the entire service flow.
- **Characteristics:** Slower than unit tests due to more complex setups and external dependencies (or their mocks). They catch issues related to interfaces and communication between parts of the system.

---

## 2. Unit Testing in Python with Pytest

### Pytest Framework
- **Installation:** Pytest is installed as a development dependency.
- **Test Discovery:** 
  - Looks for files starting with `test_` or ending with `_test.py`.
  - Within these files, it looks for functions or methods named `test_`.
  - Test files are typically organized in a dedicated `tests` folder.

### Writing Unit Tests
- **Refactoring for Testability:** Code is often refactored to make individual components easier to test in isolation.
- **Assertions:** Pytest uses Python's built-in `assert` statement to check conditions.
- **Mocking Dependencies:** External dependencies are "mocked" to keep unit tests fast and independent.
  - Example: A `ModelMock` class can simulate a real model's behavior for testing.

### Running Unit Tests from the Command Line
- A successful run typically shows dots (`.`) for passing tests.

### Setting up Pytest in Visual Studio Code (VS Code)
1. Install the official Python extension.
2. Select the correct Python interpreter (e.g., pipenv environment).
3. Configure Python tests:
   - Go to the Testing view (beaker icon).
   - Click "Configure Python Tests".
   - Select pytest as the test framework.
   - Specify the directory containing your tests.
   - VS Code will discover and list your tests for easy execution.

---

## 3. Integration Testing with Docker

- **Running Service in Docker:** Package the service into a Docker image and run as a container.
- **Sending Requests and Verifying Responses:** Use a separate Python script to send requests and verify responses.
- **DeepDiff for Detailed Comparisons:** 
  - Install with `pip install deepdiff`.
  - Use `DeepDiff(actual_response, expected_response)` for detailed comparison.
  - Supports floating-point tolerance for prediction outputs.

### Removing External Dependencies (e.g., S3)
1. Download models locally.
2. Mount local folder into Docker container using the `-v` flag.
3. Configure the application to load from a local path if specified.

### Automating Tests with Shell Scripts (`run.sh`)
1. Change directory to script location.
2. Build Docker image.
3. Start services with Docker Compose.
4. Wait for services to start.
5. Run tests.
6. Stop services after tests complete.
7. Capture and propagate exit codes for CI/CD reliability.

---

## 4. Testing AWS Services Locally with LocalStack

- **Why LocalStack?**
  - Avoid AWS costs.
  - Enable offline testing.
  - Remove dependency on internet and AWS permissions.
  - Facilitate testing complex AWS workflows locally.

- **Installation/Setup:** Run LocalStack via Docker Compose.

- **Interacting with LocalStack:**
  - **AWS CLI:** Use `--endpoint-url` to direct commands to LocalStack.
  - **Application Code (Python/Boto3):** Set the endpoint URL for AWS clients.
    - Within Docker Compose, services can refer to each other by service name.
    - Set environment variables like `KINESIS_ENDPOINT_URL` for service endpoints.

### Testing Kinesis Integration
1. Configure Boto3 Kinesis client to connect to LocalStack.
2. Get a shard iterator for the stream.
3. Retrieve records using the shard iterator.
4. Decode the data.
5. Compare actual and expected data using DeepDiff.

### S3 Testing with LocalStack (Clarification)
- The described approach for S3 is to:
  1. Download models from S3 once.
  2. Store them locally.
  3. Mount the local directory into the Docker container.
  4. Configure the application to load models from the local path.
- This removes the runtime dependency on S3 for tests.

---

## 5. Example: Calculating Predicted Durations for a Test DataFrame

Below is an example of reading a test DataFrame from S3 (using LocalStack), applying the model, and calculating the total predicted duration:

```python
import pandas as pd
import pickle

options = {
    'client_kwargs': {
        'endpoint_url': 'http://localhost:4566'
    },
    'key': 'test',
    'secret': 'test'
}
df = pd.read_parquet('s3://nyc-duration/in/2023-01.parquet', storage_options=options)

with open('/workspaces/course-mlops-zoomcamp/06-best-practices/model/model.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']

df_test = df.copy()
df_test['duration'] = df_test.tpep_dropoff_datetime - df_test.tpep_pickup_datetime
df_test['duration'] = df_test.duration.dt.total_seconds() / 60
df_test = df_test[(df_test.duration >= 1) & (df_test.duration <= 60)].copy()
df_test[categorical] = df_test[categorical].fillna(-1).astype('int').astype('str')
df_test['ride_id'] = f'2023/01_' + df_test.index.astype('str')

dicts = df_test[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = lr.predict(X_val)

df_test['predicted_duration'] = y_pred
print(df_test[['ride_id', 'predicted_duration']])

total_predicted_duration = df_test['predicted_duration'].sum()
print(total_predicted_duration)
```

---

## 6. Frequently Asked Questions (FAQ)

**Q1: What is the primary difference between unit tests and integration tests?**  
A1: Unit tests focus on isolated components or functions, are fast, and run without external dependencies. Integration tests verify that different parts of your system work together, are slower, and require more complex setups.

**Q2: Why refactor code for testing?**  
A2: Refactoring makes components smaller and more modular, making them easier to test independently and mock dependencies.

**Q3: How does Pytest simplify Python testing?**  
A3: Pytest discovers tests automatically, uses Python's assert statement, and provides a clear way to run tests from the command line or IDEs.

**Q4: Why use a ModelMock in unit tests instead of the actual model?**  
A4: ModelMock makes tests independent of external factors, faster, and more reliable by removing the need for real models or external calls.

**Q5: How does DeepDiff help in integration testing?**  
A5: DeepDiff provides detailed comparison between complex data structures, pinpointing exact differences and supporting floating-point tolerance.

**Q6: What is LocalStack and when should I use it?**  
A6: LocalStack emulates AWS services locally. Use it to test AWS integrations without incurring costs, for offline development, and for consistent test environments.

**Q7: How do you configure an application to connect to LocalStack instead of actual AWS?**  
A7: Set the `--endpoint-url` parameter or environment variables (e.g., `AWS_ENDPOINT_URL`) to point to LocalStack.

**Q8: The source mentions downloading models from S3 locally. Is this using LocalStack for S3?**  
A8: No, the approach is to download models from AWS S3 once, store them locally, and mount the directory into the Docker container for tests. The application loads models from the local path, removing the runtime S3 dependency.
