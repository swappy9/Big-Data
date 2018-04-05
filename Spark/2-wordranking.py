from pyspark import SparkConf, SparkContext
import string

#Setting up Spark context
conf = SparkConf().setMaster("local").setAppName("1-length")
sc = SparkContext(conf = conf)


#Reading raw data with delimiter ^
rawdata = sc.textFile("Amazon_Comments.csv").map(lambda x: x.split('^'))


#Creating key value pari and removing punctuation from values
keyvaluepair2 = rawdata.map(lambda x: (x[-1], x[-2].translate({ord(char): None for char in string.punctuation}).split()))


#Flattn the list of key value pair
keyvaluepair3 = keyvaluepair2.flatMapValues(lambda x: x)


#Initializing the count of each key, value pair to 1
keyvaluepair4 = keyvaluepair3.map(lambda x: ((x[0], x[1]),1))


#Counting the frequency of each key, value pair
keyvaluepair5 = keyvaluepair4.reduceByKey(lambda x, y: x + y)


#Creating key, value pair where key = star rating and value is (Count of word with respect to star rating, word)
keyvaluepair6 = keyvaluepair5.map(lambda x: (x[0][0], (x[1], x[0][1])))


#Sorting the values and taking the top 10 words based on frequency
keyvaluepair7 = keyvaluepair6.groupByKey()\
                             .mapValues(lambda x: list(x))\
                             .map(lambda x: (x[0], sorted(x[1], reverse=True)[0:10]))\
                             .sortByKey() 



#Printing the results
print 'Top 10 common words'\
      + '\n' + str(keyvaluepair7.collect()[0][0]) + ' star rating :  ' + str(keyvaluepair7.collect()[0][1]) \
      + '\n' + str(keyvaluepair7.collect()[1][0]) + ' star rating :  ' + str(keyvaluepair7.collect()[1][1]) \
      + '\n' + str(keyvaluepair7.collect()[2][0]) + ' star rating :  ' + str(keyvaluepair7.collect()[2][1]) \
      + '\n' + str(keyvaluepair7.collect()[3][0]) + ' star rating :  ' + str(keyvaluepair7.collect()[3][1]) \
      + '\n' + str(keyvaluepair7.collect()[4][0]) + ' star rating :  ' + str(keyvaluepair7.collect()[4][1]) 



