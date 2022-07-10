library(sf)
library(ggplot2)

# read csv of bounding boxes
df = read.table('trains-data/bounding_box_coordinates_ans.csv', sep = ",", header = T)

# convert bounding box values from pixels to meters
df[,2:5] = df[,2:5] * 0.1
head(df)

# convert bounding box values to coordinates
m = matrix(unlist(strsplit(df$img_name, "_")), ncol=4, byrow=T)
for ( i in 1:dim(m)[1]){

  m[[i,4]] = gsub(".tiff","", m[[i,4]])
  
}
m <- matrix(as.numeric(m), ncol = ncol(m))
colnames(m) = c("x1", "y1", "x2", "y2")
df$bbx1 = m[,c("x1")]
df$bbx2 = m[,c("x2")]
df$bby1 = m[,c("y1")]
df$bby2 = m[,c("y2")]

df$x1 = df$bbx1 + df$x1
df$x2 = df$bbx2 + df$x2
df$y1 = df$bby1 + df$y1
df$y2 = df$bby2 + df$y2
head(df)

# compute centroid of detections

x_centroid = c()
y_centroid = c()
for (i in 1:nrow(df)){

  x_centroid[i] = mean(df$x1[i], df$x2[i])
  y_centroid[i] = mean(df$y1[i], df$y2[i])
}

# write to GeoJSON
pts = st_as_sf(data.frame(cbind(x_centroid, y_centroid)), coords = c("x_centroid","y_centroid"),
               crs = "EPSG:2056")
pts$class = 'zug'
st_write(pts, 'trains-data/detected-centroid.geojson', driver = "GeoJSON")

# comparison with connection quality
qual = st_read('trains-data/quaility-transport.geojson')
qual$Klasse = unclass(as.factor(qual$Klasse))

png('fig/qual_centroids.png')
ggplot() + geom_sf(data = qual, aes(fill = Klasse)) + 
  scale_fill_gradientn(colours = sf.colors(20)) +
  theme(panel.grid.major = element_line(colour = "white"))+
  geom_sf(data = pts, fill = NA, col = "black")
dev.off()

# count points
int = st_intersection(qual, pts)
agg = aggregate(int, by=list(int$Klasse), length)

df_cor = data.frame(agg)

png('fig/correlation.png')
colnames(df_cor) = c("Class", "Detected Trains", "geometry", "etc")
ggplot(data=df_cor, aes(x=Class, y=`Detected Trains`)) +
  geom_bar(stat="identity")
dev.off()
