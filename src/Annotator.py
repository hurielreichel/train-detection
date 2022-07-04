import os
import geopandas as gpd

files = os.listdir('training_images')
#files = os.listdir('C:\\Users\\yalej\\OneDrive\\Documents\\Msc\\AnalysisHigh\\FinalProject\\training_images')
layer = gpd.read_file("labels.geojson")
#layer = gpd.read_file("C:\\Users\\yalej\\OneDrive\\Documents\\Msc\\AnalysisHigh\\FinalProject\\labels.geojson")
layer = (layer.loc[layer['class']=='zug']).reset_index(drop=True)
layer['area'] = layer.area
layer = layer.loc[layer['area']>6]
layer.reset_index(inplace=True,drop=True)

files2 = [x.replace(".tiff","") for x in files]

annotation = []

for i in range(len(layer)):
    minx = int(layer.bounds.iloc[i].minx)
    miny = int(layer.bounds.iloc[i].miny)
    maxx = int(layer.bounds.iloc[i].maxx)
    maxy = int(layer.bounds.iloc[i].maxy)

    for j in range(len(files2)):
        q=files2[j]
        if (minx >= int(q.split("_")[0])) & (maxx <= int(q.split("_")[2]) )\
                & (miny >= int(q.split("_")[1]) )& (maxy <= int(q.split("_")[3])):
            minx2 = minx - int(q.split("_")[0])
            maxx2 = maxx - int(q.split("_")[0])
            miny2 = int(q.split("_")[3]) - maxy
            maxy2 = int(q.split("_")[3]) - miny
            annotation.append(
                'training_images/' + files[j] +","+ str(minx2) +","+str(miny2)+","+str(maxx2)+","+str(maxy2)+ "," + layer.iloc[i]['class'])
            break

textfile = open("annotation.txt", "w")
for element in annotation:
    textfile.write(element + "\n")
textfile.close()
