import os
import geopandas as gpd

files = os.listdir('training_images')
#files = os.listdir('C:\\Users\\yalej\\Documents\\Msc\\AnalysisHigh\\FinalProject\\training_images')
layer = gpd.read_file("labels.geojson")
#layer = gpd.read_file("C:\\Users\\yalej\\Documents\\Msc\\AnalysisHigh\\FinalProject\\labels.geojson")
layer = (layer.loc[layer['class']=='zug']).reset_index(drop=True)
layer['area'] = layer.area
layer = layer.loc[layer['area']>6]
layer.reset_index(inplace=True,drop=True)

files2 = [x.replace(".tiff","") for x in files]

annotation = []

for i in range(len(layer)):
    minx = layer.bounds.iloc[i].minx
    miny = layer.bounds.iloc[i].miny
    maxx = layer.bounds.iloc[i].maxx
    maxy = layer.bounds.iloc[i].maxy

    for j in range(len(files2)):
        q=files2[j]
        if (minx >= float(q.split("_")[0])) & (maxx <= float(q.split("_")[2]) )\
                & (miny >= float(q.split("_")[1]) )& (maxy <= float(q.split("_")[3])):
            minx2 = minx - float(q.split("_")[0])
            maxx2 = maxx - float(q.split("_")[0])
            miny2 = float(q.split("_")[3]) - maxy
            maxy2 = float(q.split("_")[3]) - miny
            annotation.append(
                'training_images/' + files[j] +","+ str(int(minx2/0.1)) +","+str(int(miny2/0.1))+","+str(int(maxx2/0.1))+","+str(int(maxy2/0.1))+ "," + layer.iloc[i]['class'])
            break

textfile = open("annotation.txt", "w")
for element in annotation:
    textfile.write(element + "\n")
textfile.close()
