🧙‍♀️ Mage AI – Beginner’s FAQ for Data Engineering and ML Pipelines
❓ What is Mage AI?
Mage is a modern open-source data pipeline tool that bridges the power of notebooks with the structure of modular, maintainable code. It enables data teams to build real-time and batch pipelines with ease using Python, SQL, or R. The name "Mage" is inspired by magic, representing the use of advanced, seamless technology.

⚙️ What Can You Do with Mage?
Extract & sync data from third-party sources

Transform data in real-time or batch using familiar languages

Load data into warehouses or lakes using pre-built connectors

Orchestrate & monitor thousands of pipelines

Build, manage, and run dbt models

Support for streaming data ingestion and transformation

🛠️ Supported Languages
Mage allows mixing Python, SQL, and R in the same pipeline for maximum flexibility.

🧱 Mage Core Concepts
Project: Like a Git repo—stores all your code

Pipeline: A collection of executable blocks

Block: A modular unit of code

Data Product: The output of a block, which can be versioned and cataloged

Trigger: Specifies when or how a pipeline runs (e.g., schedule, API)

Run: Stores execution metadata for blocks or pipelines

📐 Design Principles
Easy dev experience via local or cloud setup

Modular & reusable code (no "throwaway" scripts)

Data is treated as a first-class citizen

Built for scale: integrates with Spark & cloud providers

📈 Viewing & Monitoring Pipelines
All pipelines: /pipelines

Pipeline detail: /pipelines/[uuid]

Logs: /pipelines/[pipeline_name]/logs

Runs: /pipeline-runs

🔁 Triggers & Scheduling
Supports schedule, event, and API-based triggers

Easily paused/resumed

Highly configurable concurrency limits (project/pipeline/block level)

💾 Data Storage & Cleanup
Output variables stored on disk or in memory

Configure external storage (e.g., AWS S3, GCS)

Clean up old variables via mage clean-cached-variables

📌 Mage Versions
Self-hosted: Run locally or in your cloud

Mage Pro: Fully-managed with advanced enterprise features

References:
1. https://docs.mage.ai/introduction/overview

2. https://docs.mage.ai/design/data-pipeline-management
