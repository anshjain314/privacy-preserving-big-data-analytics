# 🔒 Privacy Preserving Big Data Analytics in Cloud Computing

> A cloud-native privacy-preserving analytics platform that enables organizations to perform distributed big data analytics without exposing Personally Identifiable Information (PII).

---

## 🌐 Live Demo

**Dashboard:** [privacy-preserving-big-data-analytics.streamlit.app](https://privacy-preserving-big-data-analytics.streamlit.app/)

Run the full pipeline live — upload your own CSV or use the bundled 100,000-record synthetic banking dataset to see adaptive privacy protection and analytics end-to-end.

---

## 📌 Overview

Financial institutions generate massive volumes of customer data every day. While this data is valuable for analytics, it also contains highly sensitive Personally Identifiable Information (PII) such as names, Aadhaar numbers, PAN numbers, phone numbers, and addresses.

This project introduces an **Adaptive Privacy Engine** — powered by XGBoost classifiers trained to detect and classify sensitive columns — that automatically transforms sensitive information before analytics are performed.

The protected dataset is stored in **AWS S3**, processed using **Apache Spark**, and analyzed through distributed analytics modules for:

- 📊 Descriptive Analytics
- 🚨 Fraud Analytics
- 💳 Credit Risk Analysis
- 👥 Customer Segmentation

The system ensures that **no raw PII is exposed during analytical processing**, enabling privacy-preserving cloud analytics.

---

# 🏗 System Architecture

```
                   Raw Banking Dataset
                           │
                           ▼
                Adaptive Privacy Engine
     (XGBoost PII Classification + Safety-Net Rules
              + Privacy Transformation)
                           │
                           ▼
                  Protected Dataset
                           │
                           ▼
                    AWS S3 Storage
                           │
                           ▼
                  Apache Spark Cluster
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   Descriptive        Fraud Analysis    Credit Risk
    Analytics
                           │
                           ▼
               Customer Segmentation
                           │
                           ▼
               Executive Report Generator
                           │
                           ▼
              Streamlit Dashboard (Matplotlib)
                           │
                           ▼
                    Business Users
```

---

# ✨ Features

## 🔐 Adaptive Privacy Engine

- ML-based PII detection (XGBoost, trained on ~25 structural/keyword/regex features per column)
- Sensitive column identification across 16 PII categories
- 6 privacy transformation strategies: Keep, Hash, Tokenize, Pseudonymize, Bucketize, Generalize
- Rule-based safety-net overrides on top of the ML model for critical fields
- Secure protected dataset generation

---

## ☁ Cloud Integration

- AWS S3 storage via `boto3`
- Cloud-based dataset management
- Distributed data access (Spark reads directly from S3 via `s3a://`)
- Secure cloud analytics workflow

---

## ⚡ Apache Spark Analytics

Distributed analytics using PySpark:

### 📊 Descriptive Analytics
- Numeric statistics
- Customer distribution
- Account type analysis
- Card network analysis
- Income statistics
- KPI generation

### 🚨 Fraud Analytics
- Fraud rate analysis
- Fraud by account type
- Fraud by transaction channel
- Fraud vs 2FA
- Card network fraud analysis

### 💳 Credit Risk Analytics
- Loan status analysis
- Credit score statistics
- Default rate analysis
- Loan amount statistics
- KYC-based risk assessment

### 👥 Customer Segmentation
- Age segmentation
- Income segmentation
- Savings segmentation
- Premium customer identification
- Customer profiling

---

# 🛠 Technology Stack

## Programming
- Python

## Big Data
- Apache Spark
- PySpark

## Cloud
- AWS S3 (boto3)

## Machine Learning
- XGBoost
- Scikit-learn

## Data Processing
- Pandas
- NumPy

## Visualization
- Streamlit
- Matplotlib

---

# 📂 Project Structure

```
privacy-preserving-big-data-analytics/
│
├── analytics/                  # Pandas + Matplotlib analytics (used by dashboard)
│   ├── descriptive.py
│   ├── fraud.py
│   ├── credit.py
│   ├── segmentation.py
│   └── report_generator.py
│
├── privacy_engine/             # Adaptive privacy engine
│   ├── feature_builder.py
│   ├── predictor.py
│   ├── process_dataframe.py    # Orchestrates classification + safety-net overrides
│   └── transformer.py          # Applies masking strategies
│
├── feature_engineering/        # Feature extraction for model training
│   ├── feature_extractor.py
│   ├── feature_schema.py
│   └── regex_features.py
│
├── models/                     # XGBoost classifier training
│   ├── trainer.py
│   ├── train_pii_classifier.py
│   ├── train_sensitivity_classifier.py
│   ├── train_strategy_selector.py
│   └── saved_models/
│
├── generators/                 # Synthetic training data generation
│   ├── sample_generators.py
│   └── noise_generator.py
│
├── scripts/
│   └── generate_training_dataset.py
│
├── controller/
│   └── aws_manager.py          # AWS S3 integration
│
├── spark_jobs/                 # PySpark analytics (reads from S3)
│   ├── run_pipeline.py
│   ├── descriptive.py
│   ├── fraud.py
│   ├── credit.py
│   ├── segmentation.py
│   ├── config.py
│   └── utils.py
│
├── config/
│   ├── column_vocabulary.py    # Known column name variants per PII category
│   └── labels.py                # Ground-truth label rules
│
├── app.py                      # Streamlit dashboard
├── main.py                     # CLI entry point (local run)
├── requirements.txt
└── README.md
```

---

# 🔄 Workflow

```
Generate/Load Banking Dataset
          │
          ▼
XGBoost-Based PII Detection
          │
          ▼
Safety-Net Rule Overrides
          │
          ▼
Privacy Transformation
          │
          ▼
Protected Dataset
          │
          ▼
Upload to AWS S3
          │
          ▼
Spark / Pandas Analytics
          │
          ▼
Executive Report + Dashboard
```

---

# 🔐 Privacy Protection

Sensitive information is transformed before analytics. Examples include:

- Customer Name → Pseudonymized
- Aadhaar Number → Tokenized
- PAN Number → Tokenized
- Phone Number → Tokenized
- Email → Hashed
- Address → Generalized
- Bank Account Number → Tokenized
- Card Number → Tokenized
- ATM PIN Hash → Tokenized
- Date of Birth → Generalized
- Age / Salary → Bucketized

This ensures analytical processing is performed only on protected data.

---

# ⚠️ Known Limitations

- **Train/serve skew in the adaptive classifier:** The privacy engine's XGBoost models are trained on synthetically generated column names and sample values. When run against real production-style data, 2 of 57 columns (`card_number`, `loan_status`) were initially misclassified — the model's predicted strategy didn't match what the column actually needed, since the real data's value formats differed from the synthetic training distribution. A rule-based safety-net layer (`FORCE_PROTECT` / `FORCE_KEEP` in `privacy_engine/process_dataframe.py`) was added on top of the ML predictions to guarantee critical PII is always protected and business-critical analytics fields are never altered, regardless of classifier output — a standard production pattern combining adaptive ML with deterministic guardrails.
- **Fraud and credit risk modules are descriptive, not predictive** — they analyze existing labeled fields (`fraud_flag`, `loan_status`) via aggregation, rather than training a classifier to predict fraud or default from scratch.
- **PySpark jobs run on a local VM**, reading directly from S3 (`s3a://`), rather than on managed cloud infrastructure like EMR or Databricks.

---

# 🚀 Future Enhancements

- Real-time Spark Streaming
- Apache Kafka Integration
- Multi-cloud deployment
- Role-Based Access Control
- Formal k-anonymity verification
- Persisted tokenization maps for referential integrity across runs
- IAM-role-based S3 access instead of static keys
- Kubernetes support

---

# 📈 Project Highlights

- Cloud-native architecture
- ML-driven adaptive privacy protection (not just hardcoded rules)
- Distributed Spark processing with real S3 integration
- Rule-based safety-net guardrails on top of the ML model
- Scalable analytics pipeline
- Executive reporting
- Live interactive dashboard

---

# 👥 Team

**Ayush Singh · Ansh Jain · Abhishek L · Abhinav Kumar Mishra**

Bachelor of Engineering (Computer Science & Engineering)
R V Institute of Technology and Management, Bengaluru, India

**My (Ansh Jain's) contribution:** AWS S3 integration (`controller/aws_manager.py`), Streamlit dashboard (`app.py`), and debugging/fixing pipeline issues surfaced when validating against real production-style data.

---

## ⭐ If you found this project interesting, consider giving it a star.