setwd('D:/DecisionalProject')
data=read.csv(file="cleansedLyrics.csv",header=TRUE)
library("dplyr", lib.loc="~/R/win-library/3.5")
#data$Class<-ifelse(data$artist_name=="Metallica","M",ifelse(data$artist_name=="Nirvana","N",ifelse(data$artist_name=="Radiohead","R","no")))
library("e1071", lib.loc="~/R/win-library/3.5")
model <- naiveBayes(Class ~ ., data = train)
pred<-predict(model,test)
#table(pred, data$Class)
mConfusion<-table(test$Class,pred)
acc<-(mConfusion[1,1]+mConfusion[2,2]+mConfusion[3,3])/sum(mConfusion)
TrainErr<-1-acc
acc
TrainErr

#corpus <- Corpus(VectorSource(data$lyrics))
#tdm<-TermDocumentMatrix(corpus)


#sampling

library("splitstackshape", lib.loc="~/R/win-library/3.5")
test<-stratified(data,"Class", size=.3)
train<-setdiff(data,test)

train=select(train,lyrics,Class)
test=select(test,lyrics,Class)
#Training and test Matrix 
library("tm", lib.loc="~/R/win-library/3.5")
library("RTextTools", lib.loc="~/R/win-library/3.5")
library("caret", lib.loc="~/R/win-library/3.5")
train.dt_matrix<-create_matrix(train$lyrics,ngramLength=1,weighting = tm::weightTfIdf)
test.dt_matrix<-create_matrix(test$lyrics,ngramLength=1,weighting=tm::weightTfIdf,originalMatrix = train.dt_matrix)

convert_values <- function(x) {
  x <- ifelse(x > 0, "Yes", "No")
}

lyrics_train <- apply(train.dt_matrix, MARGIN = 2,
                      convert_values)
lyrics_test <- apply(test.dt_matrix, MARGIN = 2,
                     convert_values)

#SVM
svm.model<-svm(train.dt_matrix,as.factor(train$Class))
svm.predictions<-predict(svm.model,test.dt_matrix)
true.labels<-as.factor(test$Class)
mConfusion<-table(true.labels, svm.predictions)

#Bayes
library("e1071", lib.loc="~/R/win-library/3.5")
model <- naiveBayes(as.matrix(lyrics_train),as.factor(train$Class),laplace=0.5) #laplace=1
pred<- predict(model, as.matrix(lyrics_test))
true.labels<-as.factor(test$Class)
mConfusion<-table(true.labels,pred)

##trace("create_matrix",edit=T)

#view wordCloud
#Nirvana
df.Nirvana<-data %>% filter(Class== "N")
corpus <- Corpus(VectorSource(df.Nirvana$lyrics))
dtm<-TermDocumentMatrix(corpus)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
d$word <- lapply(d$word, gsub, pattern='\'', replacement='')
d$word <- lapply(d$word, gsub, pattern=',', replacement='')

#Radihohead
df.Radiohead<-data %>% filter(Class== "R")
corpusR <- Corpus(VectorSource(df.Radiohead$lyrics))
dtmR<-TermDocumentMatrix(corpusR)
mR <- as.matrix(dtmR)
vR <- sort(rowSums(mR),decreasing=TRUE)
dR <- data.frame(word = names(vR),freq=vR)

#Metallica
df.Metallica<-data %>% filter(Class== "M")
corpusM <- Corpus(VectorSource(df.Metallica$lyrics))
dtmM<-TermDocumentMatrix(corpusM)
mM <- as.matrix(dtmM)
vM <- sort(rowSums(mM),decreasing=TRUE)
dM <- data.frame(word = names(vM),freq=vM)

library("wordcloud", lib.loc="~/R/win-library/3.5")
set.seed(1234)
dev.new(width = 1000, height = 1000, unit = "px")
wordcloud(words = d$word, freq = d$freq, min.freq = 18,scale=c(4,.5),max.words=100, random.order=FALSE, rot.per=.5, colors=brewer.pal(8, "Dark2"))

dev.new(width = 1000, height = 1000, unit = "px")
wordcloud(words = dR$word, freq = d$freq, min.freq = 18,scale=c(4,.5),max.words=100, random.order=FALSE, rot.per=.5, colors=brewer.pal(8, "Dark2"))

dev.new(width = 1000, height = 1000, unit = "px")
wordcloud(words = dM$word, freq = d$freq, min.freq = 18,scale=c(4,.5),max.words=100, random.order=FALSE, rot.per=.5, colors=brewer.pal(8, "Dark2"))

#Inspect DTM
inspect(test.dt_matrix[1:10,1:10])
#Visualze columns of DTM
mat <- as.matrix(test.dt_matrix)
word_vector <- colnames(mat)