setwd("C:/Users/IBM_ADMIN/Documents/GitHub/bicimadmap/batch")
data<-read.csv('data.csv',sep=",",header=TRUE)

require(ggplot2)
require(tabplot)

#Summary
tableplot(data, cex = 1.8)
data$bases<-as.factor(data$bases)
data$zone<-as.factor(data$zone)

#KMeans clustering
fit <- kmeans(data[,c(1,2,5,6)],4)
dataC <- data.frame(data, fit$cluster)

#ScatterPlot
plotmatrix(data[,c(1,2,5,6,9,12,13)],colour=data$base)
plotmatrix(data[,c(1,2,5,6,9,12,13)],colour=data$zone)
plotmatrix(data[,c(1,2,5,6,9,12,13)],colour=fit$cluster)

pairs(data[,c(1,2,5,6,9,12,13)],col=data$base,pch=19)
pairs(data[,c(1,2,5,6,9,12,13)],col=data$zone,pch=19)
pairs(data[,c(1,2,5,6,9,12,13)],col=fit$cluster,pch=19)

#Boxplots

qplot(bases,bikes, data=data, geom=c("boxplot", "jitter"), 
      fill=bases, main="Free Bikes per Station",
      xlab="Number of bases", ylab="Bikes in deck")+ opts(axis.text.x=element_text(angle=90, hjust=1))

qplot(bases,free, data=data, geom=c("boxplot", "jitter"), 
      fill=bases, main="Free decks per Station",
      xlab="Number of bases", ylab="Free decks")+ opts(axis.text.x=element_text(angle=90, hjust=1))

qplot(zone,bikes, data=data, geom=c("boxplot", "jitter"), 
      fill=zone, main="Free Bikes per Zone",
      xlab="Number of bases", ylab="Bikes in deck")+ opts(axis.text.x=element_text(angle=90, hjust=1))

qplot(zone,free, data=data, geom=c("boxplot", "jitter"), 
      fill=zone, main="Free decks per Zone",
      xlab="Number of bases", ylab="Free decks")+ opts(axis.text.x=element_text(angle=90, hjust=1))

#Density functions
qplot(free, data=data, geom="density", fill=bases, alpha=I(.5), 
      main="Distribution of Free bikes per Station type", xlab="Free Decks", 
      ylab="Density")

qplot(bikes, data=data, geom="density", fill=bases, alpha=I(.5), 
      main="Distribution of Free decks per Station type", xlab="Free Bikes", 
      ylab="Density")

qplot(free, data=data, geom="density", fill=zone, alpha=I(.5), 
      main="Distribution of Free bikes per Zone", xlab="Free Decks", 
      ylab="Density")

qplot(bikes, data=data, geom="density", fill=zone, alpha=I(.5), 
      main="Distribution of Free decks per Zone", xlab="Free Bikes", 
      ylab="Density")
