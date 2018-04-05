from pyspark import SparkConf, SparkContext
import string

#Setting up Spark context
conf = SparkConf().setMaster("local").setAppName("1-length")
sc = SparkContext(conf = conf)


#Reading raw data with delimiter ^
rawdata = sc.textFile("Amazon_Comments.csv").map(lambda x: x.split('^'))


#Creating key value pari and removing punctuation from values
keyvaluepair2 = rawdata.map(lambda x: (x[-1], len(x[-2].translate({ord(char): None for char in string.punctuation}).split())))


#Creating broadcast variable for # of reviews for each star rating 
keycount = sc.broadcast(keyvaluepair2.countByKey())


#Creating key value pair where values = sum of words in all the comments for each star rating 
keyvaluepair3 = keyvaluepair2.reduceByKey(lambda x, y: x + y)


#Creating key value pari where value = average length of reviews for each star rating (using braodcast variable to get the total # of comments
keyvaluepair4 = keyvaluepair3.map(lambda x: (x[0], x[1]/keycount.value[x[0]])).sortByKey()


#Printing the results
print str(keyvaluepair4.collect()[0][0]) + ' star rating: average length of comments ' + str(keyvaluepair4.collect()[0][1]) \
      +'\n' +  str(keyvaluepair4.collect()[1][0]) + ' star rating: average length of comments ' + str(keyvaluepair4.collect()[1][1]) \
      +'\n' + str(keyvaluepair4.collect()[2][0]) + ' star rating: average length of comments ' + str(keyvaluepair4.collect()[2][1]) \
      +'\n' + str(keyvaluepair4.collect()[3][0]) + ' star rating: average length of comments ' + str(keyvaluepair4.collect()[3][1]) \
      +'\n' + str(keyvaluepair4.collect()[4][0]) + ' star rating: average length of comments ' + str(keyvaluepair4.collect()[4][1]) \



