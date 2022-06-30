import os
import geopandas as gpd

files = os.listdir('labels')
annotation = []


for i in files:
    #files = os.listdir(r"C:\Users\user\Documents\Msc\MachineLearningImages\src\labels")
    #i = files[0]
    shapes = os.listdir('labels/' + i)
    #shapes = os.listdir(r"C:\Users\user\Documents\Msc\MachineLearningImages\src\labels\\" + i)
    file = [x for x in shapes if x.endswith(".shp")][0]
    #layer = gpd.read_file(r"C:\Users\user\Documents\Msc\MachineLearningImages\src\labels\\" + i + '/' + file)
    layer = gpd.read_file('labels/' + i +'/'+ file)
    for j in range(len(layer)):
        if layer.area.iloc[j]<30:
            continue
        #Expand bounds


        deltax = ((layer.bounds.iloc[j].maxx- layer.bounds.iloc[j].minx)*0.15) #30% divided by 2 for each bound
        deltay = ((layer.bounds.iloc[j].maxy - layer.bounds.iloc[j].miny) * 0.15)  # 30% divided by 2 for each bound

        minx = int(layer.bounds.iloc[j].minx - deltax)
        maxx = int(layer.bounds.iloc[j].maxx - deltax)
        miny = int(layer.bounds.iloc[j].miny - deltay)
        maxy = int(layer.bounds.iloc[j].maxy - deltay)

        #compare with image (cannot have limit over the image)
        win_minx,win_miny, win_maxx,win_maxy =i.split("_")
        win_minx = int(win_minx)
        win_miny = int(win_miny)
        win_maxx = int (win_maxx)
        win_maxy = int(win_maxy)

        #otherwise standarize
        if minx<win_minx:
            minx = win_minx
        if maxx>win_maxx:
            maxx = win_maxx
        if miny<win_miny:
            miny = win_miny
        if maxy>win_maxy:
            maxy = win_maxy

        minx2 = minx - win_minx
        maxx2 = maxx - win_minx
        miny2 = win_maxy - maxy
        maxy2 = win_maxy - miny

        annotation.append('img/'+i+".tiff,"+ str(minx2) +","+str(miny2)+","+str(maxx2)+","+str(maxy2)+","+layer.iloc[0]['fclass'])


textfile = open("annotation_file.txt", "w")
for element in annotation:
    textfile.write(element + "\n")
textfile.close()
