#!/usr/bin/env python3
"""Time-ordered, leakage-aware baseline forecast on NASA GISTEMP annual anomalies."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error,mean_squared_error
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'earth-climate-analysis'/'results'/'annual_temperature_anomalies.csv'

def main():
    if not SOURCE.exists():raise SystemExit('Run ../earth-climate-analysis/analyze_earth.py with real NASA data first.')
    df=pd.read_csv(SOURCE).sort_values('year')
    # lagged anomaly features avoid using target-year observation as predictor
    for lag in range(1,6):df[f'lag{lag}']=df.anomaly_c.shift(lag)
    df=df.dropna().copy();features=[f'lag{i}' for i in range(1,6)]
    train=df[df.year<=2009];test=df[(df.year>=2010)&(df.year<=2025)]
    if len(train)<30 or len(test)<10:raise ValueError('Insufficient annual data for held-out evaluation')
    model=Ridge(alpha=1.0).fit(train[features],train.anomaly_c)
    pred=model.predict(test[features]);baseline=test.lag1.to_numpy()
    mae=mean_absolute_error(test.anomaly_c,pred);naive=mean_absolute_error(test.anomaly_c,baseline)
    rmse=np.sqrt(mean_squared_error(test.anomaly_c,pred))
    out=ROOT/'results';out.mkdir(exist_ok=True)
    pd.DataFrame({'year':test.year,'actual_anomaly_c':test.anomaly_c,'ridge_prediction_c':pred,'persistence_prediction_c':baseline}).to_csv(out/'heldout_predictions.csv',index=False)
    fig,ax=plt.subplots(figsize=(9,4.5));ax.plot(test.year,test.anomaly_c,label='Observed');ax.plot(test.year,pred,label='Ridge model');ax.plot(test.year,baseline,label='Previous-year baseline',alpha=.75);ax.legend();ax.set(xlabel='Year',ylabel='Anomaly (°C)',title='Held-out one-year-ahead prediction (2010–2025)');ax.grid(alpha=.2);fig.tight_layout();fig.savefig(out/'prediction_comparison.png',dpi=160);plt.close(fig)
    (out/'findings.md').write_text(f"""# Model evaluation on NASA GISTEMP observations
Training years: {int(train.year.min())}–{int(train.year.max())}; held-out test years: {int(test.year.min())}–{int(test.year.max())}.
Ridge MAE: {mae:.3f} °C; Ridge RMSE: {rmse:.3f} °C.
Persistence (previous year) MAE: {naive:.3f} °C.

The test split is chronological, not random. This is a simple lagged statistical forecast, not a physics-based climate model. It does not predict future emissions or establish climate causation. Lagged features use observed preceding years, including within the held-out period (one-step-ahead setting).
""")
    print((out/'findings.md').read_text())
if __name__=='__main__':main()
