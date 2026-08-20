
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
