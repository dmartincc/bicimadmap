setwd("C:/Users/IBM_ADMIN/Documents/GitHub/bicimadmap/batch")
data<-read.csv('dataDemand.csv',sep=",",header=TRUE)

require(ggplot2)
require(tabplot)
tableplot(data, cex = 1.8)

dataModel <- data[,c(4,5,8,10,12,16,18,19,20,11)]

tableplot(dataModel, cex = 1.8)

# splitdf function will return a list of training and testing sets
splitdf <- function(dataframe, size, seed=NULL) {
  if (!is.null(seed)) set.seed(seed)
  index <- 1:nrow(dataframe)
  testindex <- sample(index, trunc(length(index)/size))
  trainset <- dataframe[-testindex, ]
  testset <- dataframe[testindex, ]
  list(trainset=trainset,testset=testset)
}

splits <- splitdf(dataModel,size=10, seed=10)
train <- splits$trainset
test <- splits$testset

library(randomForest)
clf <- randomForest(train$occupyBikes ~ ., data=train,ntree=20, nodesize=5, mtry=9)
print(clf)

#R2 and MSE
(r2<- 1 - sum((test$occupyBikes-predict(clf, test))^2)/sum((test$occupyBikes-mean(test$occupyBikes))^2))
(mse <- mean((test$occupyBikes - predict(clf, test))^2))

#Regression Graph
p <- ggplot(aes(x=actual, y=pred),data=data.frame(actual=test$occupyBikes, pred=predict(clf, test)))
p + geom_point() +
  geom_abline(color="red") +
  ggtitle(paste("RandomForest Regression - R^2 = ", round(r2,2), sep=""))

#Trees performance
par(mfrow = c(1, 2))
varImpPlot(clf, pch = 19)
title(main = "Contribution of predictor variables", ylab = "Predictor variables")
plot(clf)
title(main = " Misclassification error rates ")

library(pmml)
sink("bicimadmapPredictionModel.pmml")
cat("<?xml version=\"1.0\"?>\n")
pmml(clf)
sink()
