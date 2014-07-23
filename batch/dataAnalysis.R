setwd("C:/Users/IBM_ADMIN/Documents/GitHub/bicimadmap/batch")
data<-read.csv('dataStations.csv',sep=",",header=TRUE)

require(ggplot2)
require(tabplot)
summary(data)
#Summary
tableplot(data, cex = 1.8)
data$bases<-as.factor(data$bases)
factorToNumeric <- function(f) as.numeric(levels(f))[as.integer(f)] 
cols <- c(1,2,4,5,8,12,11)
data[cols] <- as.numeric(as.matrix(data[cols]))
lapply(data, class)

data<-data[complete.cases(data),]
dataN<-data[cols]
lapply(dataN, class)



#KMeans clustering
fit <- kmeans(dataN,4)
dataC <- data.frame(dataN, fit$cluster)

#ScatterPlot
plotmatrix(data[,c(1,2,5,6,9,12,13)],colour=data$base)
plotmatrix(data[,c(1,2,5,6,9,12,13)],colour=data$zone)
plotmatrix(data[,c(1,2,5,6,9,12,13)],colour=fit$cluster)

pairs(data[,c(1,2,5,6,9,12,13)],col=data$base,pch=19)
pairs(data[,c(1,2,5,6,9,12,13)],col=data$zone,pch=19)
pairs(data[,c(1,2,5,6,9,12,13)],col=fit$cluster,pch=19)

#t-distributed stochastic neighbor embedding
require(tsne)
colors = rainbow(length(unique(data$bases)))
names(colors) = unique(data$bases)
ecb = function(x,y){ plot(x,t='n'); text(x,labels=data$name, col=colors[data$bases]) }
tsne_iris = tsne(dataN, epoch_callback = ecb, perplexity=50)


#Boxplots

qplot(bases,occupyRate, data=dataC, geom=c("boxplot", "jitter"), 
      fill=bases, main="Free Bikes per Station",
      xlab="Rate", ylab="Bases in deck",colour=fit.cluster)+ opts(axis.text.x=element_text(angle=90, hjust=1))

qplot(bases,free, data=dataC, geom=c("boxplot", "jitter"), 
      fill=bases, main="Free decks per Station",
      xlab="Number of bases", ylab="Free decks",colour=fit.cluster)+ opts(axis.text.x=element_text(angle=90, hjust=1))

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
