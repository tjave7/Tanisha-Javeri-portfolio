#!/usr/bin/env python3
"""Compute Chicago Landsat 8/9 Collection 2 Level-2 NDVI from real, aligned bands.
No simulated satellite imagery. Inputs must be actual USGS red/NIR raster pairs.
"""
import argparse
from pathlib import Path
import numpy as np
import rasterio
import matplotlib.pyplot as plt

def ndvi(red_path,nir_path):
    with rasterio.open(red_path) as red, rasterio.open(nir_path) as nir:
        if (red.crs,red.transform,red.shape)!=(nir.crs,nir.transform,nir.shape):
            raise ValueError('Band grids do not match; align/reproject before analysis.')
        a=red.read(1).astype(float);b=nir.read(1).astype(float)
        # Landsat Collection 2 Level-2 surface reflectance scaling
        mask=(a==0)|(b==0)|(a==red.nodata)|(b==nir.nodata)
        a=a*0.0000275-0.2;b=b*0.0000275-0.2
        denom=a+b
        with np.errstate(divide='ignore',invalid='ignore'):
            result=(b-a)/denom
        result[mask|(~np.isfinite(result))|(denom==0)]=np.nan
        return result,red.profile

def main():
    parser=argparse.ArgumentParser(description='NDVI comparison using actual Landsat SR_B4 and SR_B5 GeoTIFFs')
    for name in ['early_red','early_nir','late_red','late_nir']:parser.add_argument('--'+name.replace('_','-'),required=True)
    a=parser.parse_args()
    first,profile=ndvi(a.early_red,a.early_nir);last,profile2=ndvi(a.late_red,a.late_nir)
    if first.shape!=last.shape or profile['transform']!=profile2['transform'] or profile['crs']!=profile2['crs']:
        raise ValueError('Dates must be co-registered to same grid, extent and CRS.')
    out=Path(__file__).resolve().parent/'results';out.mkdir(exist_ok=True)
    diff=last-first
    valid=np.isfinite(diff)
    if not valid.any():raise ValueError('No comparable valid pixels')
    profile.update(dtype='float32',count=1,nodata=-9999)
    for name,data in [('early_ndvi',first),('late_ndvi',last),('ndvi_change',diff)]:
        with rasterio.open(out/f'{name}.tif','w',**profile) as dst:dst.write(np.where(np.isfinite(data),data,-9999).astype('float32'),1)
    fig,ax=plt.subplots(figsize=(7,6));im=ax.imshow(np.ma.masked_invalid(diff),vmin=-.5,vmax=.5,cmap='RdYlGn');fig.colorbar(im,ax=ax,label='NDVI difference');ax.set(title='NDVI change: later minus earlier',xticks=[],yticks=[]);fig.tight_layout();fig.savefig(out/'ndvi_change.png',dpi=160);plt.close(fig)
    (out/'findings.md').write_text(f"""# Chicago vegetation change — measured imagery
Valid comparison pixels: {int(valid.sum())}
Mean NDVI change: {np.nanmean(diff):.3f}
Median NDVI change: {np.nanmedian(diff):.3f}

## Limitations
The input imagery must cover the same area, be co-registered, cloud-masked, and represent comparable growing-season dates. This script masks Landsat fill values but does NOT perform QA_PIXEL cloud/shadow masking. Until that step is done, results are exploratory and may be biased by clouds, snow, water and seasonal differences. NDVI is a vegetation index, not a direct measure of biodiversity or plant health.
""")
    print('Results written to',out)
if __name__=='__main__':main()
