import pandas as pd
import wget
import os
import shutil
import geopandas as gpd

from pathlib import Path

# download list of counties
countries = pd.read_csv("https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv")
countries = countries[countries["region"]=="Europe"]

# create temporary folder for downloaded files
os.mkdir("zip")

# download
for i, code in enumerate(countries["alpha-3"]):
    print(f"downloading {code} ({i+1}/{len(countries)})")
    wget.download(f"https://biogeo.ucdavis.edu/data/diva/rrd/{code}_rrd.zip", out="zip")
    print()
    
#concatenate
print("concatenating...")
folder = Path("zip")
shapefiles = folder.glob("*.zip")
gdf = pd.concat(
    [gpd.read_file("zip://" + str(shp)) for shp in shapefiles]).pipe(gpd.GeoDataFrame)
gdf.to_file('rail_europe.shp')

#remove working files
shutil.rmtree("zip")

print("done")

