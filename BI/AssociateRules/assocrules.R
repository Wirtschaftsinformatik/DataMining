#a<-'A,B'
#a<-rbind(a,'A')
#a<-rbind(a,'A,B')
#a<-rbind(a,'B,D,E')
#a<-rbind(a,'A,C,D')
#a<-rbind(a,'C,E')
#a<-rbind(a,'B,C,E')
#a<-rbind(a,'A,C,D,E')
#a<-rbind(a,'B,D')
#a<-rbind(a,'D')
#a<-rbind(a,'B,E')
#write.table(a,file="test.csv", row.names=F, col.names=F, quote=F)


# install and load packages ####
# install.packages("arules")
# install.packages("arulesViz")
library(arulesViz)
library(arules)

# load data ####
# simple set
setwd('/home/ci95poh/Desktop/Übung')
tr<-read.transactions(file="Alphabet.csv",format="basket",sep=",")
# standard data set
# data("Groceries")
# tr <- Groceries

# get first impression
summary(tr)
inspect(tr)

itemFrequencyPlot(tr)
image(tr)

# get support for 2. sample
inspect(tr[2])
support(tr[2],tr)

# calc and display rules
rules <- apriori(tr,parameter = list(supp = 0.1, conf = 0.5))
rules <- apriori(tr,parameter = list(supp = 0.05, conf = 0.001))
head(inspect(rules))

plot(rules, measure = c("support", "confidence"), shading = "lift")
plot(rules, measure = c("support", "confidence"), shading = "lift", jitter=2)
plot(rules, measure = c("support", "lift"), shading = "confidence")
plot(rules, method = "paracoord", control=list( reorder=TRUE))


subrules2 <- head(sort(rules, by="lift"), 10)
plot(subrules2, measure = c("support", "confidence"), shading = "lift", jitter=2)
plot(subrules2, measure = c("support", "lift"), shading = "confidence")
plot(subrules2, method = "paracoord", control=list( reorder=TRUE))
