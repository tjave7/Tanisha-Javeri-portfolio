# Machine Learning for Annual Climate Anomaly Prediction

Runs only after the Earth Climate project has downloaded and processed real NASA GISTEMP data. Ridge regression with five lagged annual anomalies; chronological train through 2009 and test 2010–2025. Compares against a previous-year persistence baseline. Run `pip install -r requirements.txt && python train_model.py`.

**Status:** Implemented, awaiting real NASA CSV for measured evaluation. Do not claim model accuracy before execution.
