"""Reproduce verified plots from a carefully attributed 24-month NASA GISTEMP excerpt."""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
base=Path(__file__).parent
df=pd.read_csv(base/'nasa_gistemp_excerpt_2024_2026.csv')
y=df.global_temperature_anomaly_c.to_numpy()
x=np.arange(len(y))
print('Short-window slope C/year:',np.polyfit(x,y,1)[0]*12)
plt.plot(df.month,y,marker='o');plt.xticks(rotation=75);plt.tight_layout();plt.savefig(base/'earth_climate_observed.png',dpi=170);plt.close()
X=np.array([y[i-3:i] for i in range(3,len(y))]); target=y[3:]; cut=len(target)-6
model=Ridge(alpha=1).fit(X[:cut],target[:cut]); pred=model.predict(X[cut:]); naive=X[cut:,-1]
print('Ridge MAE',mean_absolute_error(target[cut:],pred),'Baseline MAE',mean_absolute_error(target[cut:],naive))
plt.plot(df.month.iloc[-6:],target[cut:],label='Observed');plt.plot(df.month.iloc[-6:],pred,label='Ridge');plt.plot(df.month.iloc[-6:],naive,label='Baseline');plt.legend();plt.tight_layout();plt.savefig(base/'climate_ml_evaluation.png',dpi=170)
