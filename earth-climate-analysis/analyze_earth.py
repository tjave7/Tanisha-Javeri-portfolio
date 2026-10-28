#!/usr/bin/env python3
"""Reproducible NASA GISTEMP global annual temperature-anomaly analysis."""
from pathlib import Path
from urllib.request import urlopen,Request
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
URL="https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"

def main():
    ROOT.joinpath('data').mkdir(exist_ok=True)
    ROOT.joinpath('results').mkdir(exist_ok=True)
    dest=ROOT/'data'/'NASA_GISTEMP_GLB.csv'
    if not dest.exists():
        try:
            with urlopen(Request(URL,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as r: dest.write_bytes(r.read())
        except Exception as exc: raise SystemExit(f'Could not download NASA observations: {exc}\nManually download {URL} to {dest}')
    # NASA CSV includes a title line and columns Year, Jan ... Dec, J-D.
    df=pd.read_csv(dest,skiprows=1, dtype=str)
    df.columns=[str(x).strip() for x in df.columns]
    if 'Year' not in df or 'J-D' not in df: raise ValueError('Unexpected NASA CSV layout; check NASA source format')
    df['year']=pd.to_numeric(df['Year'],errors='coerce')
    df['anomaly_c']=pd.to_numeric(df['J-D'].str.strip().replace('***',np.nan),errors='coerce')/100
    df=df[['year','anomaly_c']].dropna().sort_values('year')
    df=df[df.year<=2025] # only full calendar years, avoid provisional 2026
    if len(df)<30: raise ValueError('Not enough complete annual observations')
    df.to_csv(ROOT/'results'/'annual_temperature_anomalies.csv',index=False)
    recent=df[df.year>=1970]
    slope,intercept=np.polyfit(recent.year,recent.anomaly_c,1)
    fig,ax=plt.subplots(figsize=(10,5))
    ax.plot(df.year,df.anomaly_c,label='NASA GISTEMP annual anomaly')
    ax.plot(recent.year,slope*recent.year+intercept,label='Linear trend, 1970–2025')
    ax.axhline(0,color='gray',lw=.8)
    ax.set(title='Global surface temperature anomaly (1951–1980 baseline)',xlabel='Year',ylabel='Temperature anomaly (°C)')
    ax.legend();ax.grid(alpha=.25);fig.tight_layout();fig.savefig(ROOT/'results'/'earth_temperature_trend.png',dpi=170);plt.close(fig)
    (ROOT/'results'/'findings.md').write_text(f"""# Observed NASA GISTEMP analysis

Data: NASA GISTEMP v4 global annual land-ocean temperature anomaly, baseline 1951–1980.
Years included: {int(df.year.min())}–{int(df.year.max())}; {len(df)} complete years.
Linear trend for 1970–2025: {slope*10:.3f} °C per decade (descriptive ordinary least squares).
2025 anomaly: {df.loc[df.year==2025,'anomaly_c'].iloc[0]:.2f} °C relative to the 1951–1980 average.

## Interpretation
The trend is descriptive, not a causal attribution analysis. Annual anomalies are relative to the specified reference period, not absolute global temperatures. Data may be revised by NASA.

Source: {URL}
""")
    print((ROOT/'results'/'findings.md').read_text())
if __name__=='__main__': main()
