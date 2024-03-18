# Outliers detection app

It is a REST API application that accept stock_exchange and file_paths and return a list with messages (one for each file).
If the application detects outliers in the user provided files, it creates a new "outliers_filename".csv writing the detections in "output_files" directory.

## Prerequisites

python must be installed
NOTE: Just for beeing sure, use python3.8 and above

## Set-up application Locally

1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Create Virtual Environment & run it
```bash
pip python3 -m venv .venv
source .venv/bin/activate
```

3. Run Flask application (on port 5000 in our example)
```bash
flask run --port=5000
```