import os
import pandas as pd
from osgeo import gdal,osr
import rasterio
from pyproj.crs import CRS
from rasterio.plot import show
import matplotlib
from shapely.geometry import box
from fiona.crs import from_epsg
from shapely import geometry
import geopandas as gpd
from rasterio.mask import mask
import pycrs

files = os.listdir('si-2018')
#raster = rasterio.open(os.path.join('C:\\Users\\yalej\\OneDrive\\Documents\\Msc\\AnalysisHigh\\FinalProject\\si-2018', files[0]))
mask_total= gpd.GeoDataFrame()
for file in files:
    raster = rasterio.open(os.path.join('si-2018', file))
    minx, miny = raster.bounds.left, raster.bounds.bottom
    maxx, maxy = raster.bounds.left+100, raster.bounds.bottom+100
    raster.close()

    min_x, max_x, min_y, max_y = minx, maxx, miny, maxy
    for i in range(10):
        miny, maxy = min_y, max_y
        for j in range (10):
            p1 = geometry.Point(minx,miny)
            p2 = geometry.Point(maxx,miny)
            p3 = geometry.Point(maxx,maxy)
            p4 = geometry.Point(minx,maxy)
            pointList = [p1, p2, p3, p4, p1]

            bbox = box(minx, miny, maxx, maxy)

            mask_bb = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(2056))
            mask_total = gpd.GeoDataFrame(pd.concat([mask_total, mask_bb], ignore_index=True),crs=from_epsg(2056))

            miny, maxy = miny + 100, maxy + 100
        minx, maxx = minx + 100, maxx + 100

mask_total = mask_total.set_crs(epsg=2056)
mask_total = mask_total.drop_duplicates()
mask_total.reset_index(inplace=True, drop=True)
mask_total.to_file("bounding_box.geojson", driver='GeoJSON')

def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

for file in files:
    img = rasterio.open(os.path.join('si-2018', file))
    for i in range(len(mask_total)):
        coords = getFeatures(mask_total.loc[mask_total.index==i])
        try:
            out_img, out_transform = mask(dataset=img, shapes=coords, crop=True)
        except:
            continue
        out_meta = img.meta.copy()
        epsg_code = int(img.crs.data['init'][5:])
        out_meta.update({"driver": "GTiff", "height": out_img.shape[1], "width": out_img.shape[2],
                       "transform": out_transform, "crs": CRS.from_epsg(2056)})
        with rasterio.open("training_images/{}_{}_{}_{}.tiff".format(int(mask_total.loc[mask_total.index==i].bounds.minx),
                                                                     int(mask_total.loc[mask_total.index==i].bounds.miny),
                                                                     int(mask_total.loc[mask_total.index==i].bounds.maxx),
                                                                     int(mask_total.loc[mask_total.index==i].bounds.maxy)),
                           "w", **out_meta) as dest:
            dest.write(out_img)
    img.close()

labels = gpd.read_file("vehicles-labels.geojson")
labels_inter = gpd.overlay(labels, mask_total)
labels_inter.to_file("labels.geojson", driver='GeoJSON')



################################################################################33

'''files = os.listdir('C:\\Users\\yalej\\OneDrive\\Documents\\Msc\\AnalysisHigh\\FinalProject\\si-2018')
raster = gdal.Open(os.path.join('all-images-256', files[0]))
raster = gdal.Open(os.path.join('C:\\Users\\user\\Documents\\Msc\\AnalysisHigh\\FinalProject\\si-2018', files[0]))

raster = rasterio.open(os.path.join('C:\\Users\\user\\Documents\\Msc\\AnalysisHigh\\FinalProject\\si-2018', files[0]))
img = raster.read()

row=0
for r in range(10):
    col=0
    for c in range(10):
        img_test = img[0:3,row:row+1000,col:col+1000]
        col = col + 1000
        transform = from_origin(472137, 5015782, 0.5, 0.5)
        new_dataset = rasterio.open('C:\\Users\\user\\Documents\\Msc\\AnalysisHigh\\FinalProject\\si-2018\\test.tif', 'w',
                                    driver='GTiff',
                                    height=img_test.shape[1], width=img_test.shape[2],
                                    count=3, dtype=str(img_test.dtype),
                                    crs=CRS.from_epsg(2056))

        new_dataset.write(img_test)
        new_dataset.close()



np.array(raster.GetRasterBand(1).ReadAsArray())

files_json = [x for x in files if x.endswith(".json")]
files_img = [x for x in files if x.endswith(".tif")]

print(files_img)



for i in range(len(files_json)):
    print("this is the image number: ",i)
    df = pd.read_json("all-images-256/"+str(files_json[i]))
    #df = pd.read_json("C:\\Users\\user\\Documents\\Msc\\AnalysisHigh\\FinalProject\\all-images-256\\19_273184_183226.json")
    os.rename("all-images-256/"+files_img[i], "img/"+str(int(df.iloc[2].extent)) + "_"
              + str(int(df.iloc[4].extent)) + "_" + str(int(df.iloc[1].extent)) + "_" + str(int(df.iloc[3].extent))+".tif") '''