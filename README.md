# GenAI-Powered DSAT Root Cause Analyzer

#Try the demo app here:
https://hossain-dsat-root-cause-analyzer.streamlit.app/

This project is a privacy-safe GenAI/analytics app for customer support operations. It analyzes DSAT cases, classifies root causes, identifies agent-driven vs non-agent-driven dissatisfaction, and generates coaching recommendations and RCA dashboards.

## Business Problem

Contact centers often review DSAT cases manually. This can be slow and inconsistent. This app provides a structured workflow to classify DSAT root causes, summarize evidence, generate coaching actions, and export RCA reports.

## Key Features

- Upload CSV or Excel DSAT case files
- Use bundled synthetic DSAT dataset for demo
- Select transcript/comment/QA note columns
- Classify DSAT into:
  - Agent-Driven DSAT
  - Non-Agent-Driven DSAT
  - Mixed Accountability
  - Needs QA Validation
- Identify root cause category, severity, confidence, evidence, coaching action, and recovery action
- Interactive Streamlit dashboard
- Download analyzed CSV and Excel RCA report
- Optional OpenAI mode using Streamlit Secrets
- Rule-based demo mode works without API keys

## Why Synthetic Data?

The dataset in this repository is synthetic and does not contain real customer, company, agent, or client information. It was created to preserve realistic DSAT patterns while protecting confidentiality.

## Project Structure

```text
dsat-root-cause-analyzer/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── data/
│   └── synthetic_dsat_cases.csv
├── src/
│   ├── config.py
│   ├── preprocessing.py
│   ├── rules.py
│   ├── prompts.py
│   ├── llm_client.py
│   ├── dsat_analyzer.py
│   ├── dashboard.py
│   ├── evaluation.py
│   └── report_generator.py
└── notebooks/
    └── colab_end_to_end_pipeline.ipynb
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```


## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app.
4. Choose your GitHub repo, branch, and `app.py` as the main file.
5. Make sure `requirements.txt` is in the repository root.
6. Optional: add `OPENAI_API_KEY` in Streamlit app secrets.
7. Deploy.

## Evaluation

The synthetic dataset includes `human_label`, so the app can calculate a basic agreement score between the classifier output and the provided labels.

## Limitations

- Rule-based demo mode is intentionally simple.
- LLM output should not be used as the final basis for agent performance action without QA/TL review.
- Real production use should include human-in-the-loop validation, calibration, and policy grounding.

