from pyspark import SparkContext
from pyspark import sql
from pyspark.sql import SQLContext, Row, functions as F
from pyspark.sql.functions import *
from pyspark.sql.types import StringType
import string
import re
from collections import Counter
from collections import OrderedDict
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")

sc = SparkContext()
sqlContext = sql.SQLContext(sc)

#Reading review and business files
review = sqlContext.read.format('com.databricks.spark.csv').options(header='true',inferschema='true', delimiter='^').load('yelp_review_short.csv')
business = sqlContext.read.format('com.databricks.spark.csv').options(header='true',inferschema='true', delimiter='^').load('yelp_business_sector_new.csv')


#review = sc.textFile("yelp_review_short.csv").map(lambda x: x.split('^'))
#header = review.first()
#review1 = review.filter(lambda x: len(x[0]) > 35)

#Filtering any null values from review file
df = review.filter(review.review_id.isNotNull())\
		.filter(review.user_id.isNotNull())\
		.filter(review.business_id.isNotNull())\
		.filter(review.stars.isNotNull())\
		.filter(review.date.isNotNull())\
		.filter(review.text.isNotNull())\
		.filter(review.useful.isNotNull())\
		.filter(review.funny.isNotNull())\
		.filter(review.cool.isNotNull())

#Taking required columns from Business file & rename business and star column
df1 = business.select(col('business_id').alias('bus_business_id'), 'name', 'neighborhood', 'city', 'state', 'postal_code', col("stars").alias("business_stars"), 'review_count', 'is_open', 'Cate')


#Merging the 2 dataframes on business_id
review_business = df.join(df1, df.business_id == df1.bus_business_id)

#Remove punctuation from text column
#text_rm = regexp_replace(review_business.text, re.sub,"")
text_rm = regexp_replace(review_business.text, "[{0}]".format(re.escape(string.punctuation)),"")
review_business = review_business.withColumn("text_cleaned", text_rm)

#Adding column length of review text
split_col = split(review_business.text_cleaned, " ")
review_business = review_business.withColumn("review_words", split_col)
review_business = review_business.withColumn("review_length", size(split_col))
review_business = review_business.select('review_id', 'user_id', 'business_id', 'stars', 'date', 'text', 'useful', 'funny', 'cool', 'bus_business_id',\
					 'name', 'neighborhood', 'city', 'state', 'postal_code', 'business_stars', 'review_count', 'is_open', 'Cate',\
					 'review_words', 'review_length', year("date").alias("year"), month("date").alias("month"),'text_cleaned')


#Distribution of words based on city/business/star

def tokenization(eachline):
	text = eachline[1].lower().strip().split(" ")
	wcount = Counter(text)
	return (eachline[0], wcount)
stop = set(stopwords.words("english"))

review_wf_city = review_business.groupBy("city").agg(concat_ws(",",collect_list("text_cleaned")).alias('group_text'))
review_wf_city = review_wf_city.rdd.map(list).map(tokenization)
review_wf_city = review_wf_city.map(lambda x: (x[0],[i for i in x[1].items() if i[0] not in stop]))
review_wf_city = review_wf_city.reduceByKey(lambda x,y: (x+y))
rating_sorted_city = review_wf_city.map(lambda x: (x[0],sorted(x[1],key=lambda y: y[1], reverse=True)))
review_wf_city = rating_sorted_city.map(lambda x: (x[0], [i for i in x[1] if i not in stop][:50]))


review_wf_business = review_business.groupBy("Cate").agg(concat_ws(",",collect_list("text_cleaned")).alias('group_text'))
review_wf_business = review_wf_business.rdd.map(list).map(tokenization)
review_wf_business = review_wf_business.map(lambda x: (x[0],[i for i in x[1].items() if i[0] not in stop]))
review_wf_business = review_wf_business.reduceByKey(lambda x,y: (x+y))
rating_sorted_bus = review_wf_business.map(lambda x: (x[0],sorted(x[1],key=lambda y: y[1], reverse=True)))
review_wf_business = rating_sorted_bus.map(lambda x: (x[0],[i for i in x[1] if i not in stop][:50]))


def tokenization_2(eachline):
	text = eachline[2].lower().strip().split(" ")
	wcount = Counter(text)
	return ((eachline[0], eachline[1]),wcount)

review_wf_bus_star = review_business.groupBy(["Cate","stars"]).agg(concat_ws(",",collect_list("text_cleaned")).alias('group_text'))
review_wf_bus_star = review_wf_bus_star.rdd.map(list).map(tokenization_2)
review_wf_bus_star = review_wf_bus_star.map(lambda x: (x[0],[i for i in x[1].items() if i[0] not in stop]))
review_wf_bus_star = review_wf_bus_star.reduceByKey(lambda x,y: (x+y))
rating_sorted_bus_star = review_wf_bus_star.map(lambda x: (x[0],sorted(x[1],key=lambda y: y[1], reverse=True)))
review_wf_bus_star = rating_sorted_bus_star.map(lambda x: (x[0],[i for i in x[1] if i not in stop][:50]))


#month-wise distribution of the number of star ratings
review_count_month_rating = review_business.groupBy(["month","stars"]).agg(count("review_length")).sort(review_business['month'])
#year-wise comparison of the number of star ratings for each business
review_count_year_bus_star = review_business.filter(review_business.stars == 5).groupBy(["year","Cate"]).agg(count("review_length")).sort(review_business['year'],review_business['Cate'])



#Printing the results

#print review_count_month_rating.collect()
#print review_count_year_bus_star.collect()

#print review_wf_city.take(5)
#print review_wf_business.take(5)
print review_wf_bus_star.take(5)

#Save outputs into files
#review_wf_city.saveAsTextFile("review_wf_city.csv")
#review_wf_business.saveAsTextFile("review_wf_business.csv")
review_wf_bus_star.saveAsTextFile("review_wf_bus_star.csv")
