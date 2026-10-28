#!/usr/bin/env python3
"""Analyze NASA InSight Mars Weather API measurements. No synthetic observations."""
import argparse, json, urllib.request
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

API='https://api.nasa.gov/insight_weather/?api_key=DEMO_KEY&feedtype=json&ver=1.0'
BASE=Path(__file__).resolve().parent

def download():
    request=urllib.request.Request(API,headers={'User-Agent':'StudentMarsResearch/1.0'})
    with urllib.request.urlopen(request,timeout=30) as response: data=json.load(response)
    if not data.get('sol_keys'): raise RuntimeError('NASA API returned no sol observations; supply an archived JSON file with --input.')
    (BASE/'data').mkdir(exist_ok=True)
    (BASE/'data'/'nasa_insight_raw.json').write_text(json.dumps(data,indent=2))
    return data

def unpack(data):
    rows=[]
    for sol in data.get('sol_keys',[]):
        record=data.get(str(sol),{})
        def value(sensor,stat): return record.get(sensor,{}).get(stat)
        rows.append({'sol':int(sol),'first_utc':record.get('First_UTC'),'last_utc':record.get('Last_UTC'),
          'temperature_mean_c':value('AT','av'),'temperature_min_c':value('AT','mn'),'temperature_max_c':value('AT','mx'),
          'pressure_mean_pa':value('PRE','av'),'pressure_min_pa':value('PRE','mn'),'pressure_max_pa':value('PRE','mx'),
          'temperature_samples':value('AT','ct'),'pressure_samples':value('PRE','ct')})
    if not rows: raise ValueError('No sols found in the supplied NASA data.')
    df=pd.DataFrame(rows).sort_values('sol').drop_duplicates('sol')
    for col in df.columns.difference(['sol','first_utc','last_utc']): df[col]=pd.to_numeric(df[col],errors='coerce')
    return df

def plot(df,col,ylabel,title,filename):
    valid=df[['sol',col]].dropna()
    if valid.empty: return False
    fig,ax=plt.subplots(figsize=(9,4.6))
    ax.plot(valid.sol,valid[col],marker='o',linewidth=1.7)
    ax.set(xlabel='Martian sol (mission day)',ylabel=ylabel,title=title)
    ax.grid(alpha=.25);fig.tight_layout();fig.savefig(BASE/'results'/filename,dpi=160);plt.close(fig)
    return True

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',help='Previously downloaded InSight API JSON (for reproducible offline analysis)')
    args=parser.parse_args()
    data=json.loads(Path(args.input).read_text()) if args.input else download()
    df=unpack(data); (BASE/'results').mkdir(exist_ok=True)
    df.to_csv(BASE/'results'/'cleaned_mars_weather.csv',index=False)
    plot(df,'temperature_mean_c','Temperature (°C)','InSight: daily average air temperature','temperature.png')
    plot(df,'pressure_mean_pa','Pressure (Pa)','InSight: daily average atmospheric pressure','pressure.png')
    lines=['# Mars Atmospheric Data Analysis — Observed Results','',
      'Data source: NASA InSight Mars Weather Service API (historical mission observations).',
      f'Number of sols returned: {len(df)}.',
      f'Sols in sample: {df.sol.min()}–{df.sol.max()}.','',
      '## Descriptive statistics','']
    for label,col,unit in [('Mean air temperature','temperature_mean_c','°C'),('Mean atmospheric pressure','pressure_mean_pa','Pa')]:
        x=df[col].dropna()
        lines.append(f'- {label}: {x.mean():.2f} {unit} across {len(x)} sols; range {x.min():.2f}–{x.max():.2f} {unit}.' if len(x) else f'- {label}: no measurements available.')
    lines += ['','## Interpretation and limitations',
      'These are site-specific measurements at Elysium Planitia, not a global average for Mars.',
      'The API exposes only the last seven available sols, which is insufficient to establish a seasonal or long-term trend.',
      'Missing sensor measurements are excluded from each summary; absence is not treated as zero.',
      'These data cannot establish whether Mars is habitable or whether liquid water is present.',
      'Compare environmental constraints with the separate student essay about human settlement; do not present that essay as measured evidence.','',
      'Source: https://api.nasa.gov/ (InSight Mars Weather Service).']
    (BASE/'results'/'findings.md').write_text('\n'.join(lines)+'\n')
    print('Saved results to:',BASE/'results'); print('\n'.join(lines))

if __name__=='__main__':main()
