from pyspark import SparkContext
from pyspark import sql
from pyspark.sql import SQLContext, Row, functions as F
from pyspark.sql.functions import *
import string
import re
import pandas

sc = SparkContext()
sqlContext = sql.SQLContext(sc)

#Reading review and business files
#review = sqlContext.read.format('com.databricks.spark.csv').options(header='true',inferschema='true', delimiter='^').load('yelp_review_short.csv')
review = sqlContext.read.format('com.databricks.spark.csv').options(header='true',inferschema='true').load('yelp_review_new.csv')
business = sqlContext.read.format('com.databricks.spark.csv').options(header='true',inferschema='true', delimiter='^').load('yelp_business_new_sector.csv')

print "Dataframes entered"

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
  
print "Dataframes filtered"      

df1 = business.select(col('business_id').alias('bus_business_id'), 'name', 'neighborhood', 'city', 'state', 'postal_code', col("stars").alias("business_stars"), 'review_count', 'is_open', 'Cate')

review_business = df.join(df1, df.business_id == df1.bus_business_id)


#cities = review_business.select('state').distinct().rdd.map(lambda r: r[0]).collect()

cities = [u'AZ',u'PA',u'OH',u'NV',u'NC',u'SC',u'WI',u'IL',u'ON',u'QC',u'AB']

print "Unique locations identified"  

cityCount ={}; cityResta ={}; cityHealth ={}; citySpa ={}; cityEdu ={}; cityLocal ={}; cityNight ={};
cityShop ={}; cityHotel ={}; cityGov ={}; cityEstate ={}; cityActive ={}; cityArts ={}
for i in cities:
    cityCount[i] = review_business.filter(review_business.state == i).groupby("stars").agg(count("stars"))
    cityResta[i] = review_business.filter(review_business.state == i).filter(review_business.Cate == "Restaurants").groupby("stars").agg(count("stars"))
    cityHealth[i] = review_business.filter(review_business.state == i).filter(review_business.Cate == "Health & Medical").groupby("stars").agg(count("stars"))
    citySpa[i] = review_business.filter(review_business.state == i).filter(review_business.Cate == "Beauty & Spas").groupby("stars").agg(count("stars"))
    cityEdu[i] = review_business.filter(review_business.state == i).filter(review_business.Cate == "Education").groupby("stars").agg(count("stars"))
    cityLocal[i] = review_business.filter(review_business.state == i).filter(review_business.Cate == "Local Services").groupby("stars").agg(count("stars"))
    cityShop[i] = review_business.filter(review_business.state == i).filter(review_business.Cate == "Shopping").groupby("stars").agg(count("stars"))
    cityHotel[i] = review_business.filter(review_business.state == i).filter(review_business.Cate == "Hotels & Travel").groupby("stars").agg(count("stars"))
    cityGov[i] = review_business.filter(review_business.state == i).filter(review_business.Cate == "Public Services & Government").groupby("stars").agg(count("stars"))
    cityActive[i] = review_business.filter(review_business.state == i).filter(review_business.Cate == "Active Life").groupby("stars").agg(count("stars"))
    cityNight[i] = review_business.filter(review_business.state == i).filter(review_business.Cate == "Nightlife").groupby("stars").agg(count("stars"))
    cityArts[i] = review_business.filter(review_business.state == i).filter(review_business.Cate == "Arts & Entertainment").groupby("stars").agg(count("stars"))

print "Writing to Excel"  

writerCount = pandas.ExcelWriter('cityCount.xlsx')
writerResta = pandas.ExcelWriter('cityResta.xlsx')
writerHealth = pandas.ExcelWriter('cityHealth.xlsx')
writerSpa = pandas.ExcelWriter('citySpa.xlsx')
writerEdu = pandas.ExcelWriter('cityEdu.xlsx')
writerLocal = pandas.ExcelWriter('cityLocal.xlsx')
writerShop = pandas.ExcelWriter('cityShop.xlsx')
writerHotel = pandas.ExcelWriter('cityHotel.xlsx')
writerGov = pandas.ExcelWriter('cityGov.xlsx')
writerActive = pandas.ExcelWriter('cityActive.xlsx')
writerNight = pandas.ExcelWriter('cityNight.xlsx')
writerArts = pandas.ExcelWriter('cityArts.xlsx')


for i in cities:
    print i
    cityCount[i].toPandas().to_excel(writerCount,sheet_name =i)
    cityResta[i].toPandas().to_excel(writerResta,sheet_name =i)
    cityHealth[i].toPandas().to_excel(writerHealth,sheet_name =i)
    citySpa[i].toPandas().to_excel(writerSpa,sheet_name =i)
    cityEdu[i].toPandas().to_excel(writerEdu,sheet_name =i)
    cityLocal[i].toPandas().to_excel(writerLocal,sheet_name =i)
    cityShop[i].toPandas().to_excel(writerShop,sheet_name =i)
    cityHotel[i].toPandas().to_excel(writerHotel,sheet_name =i)
    cityGov[i].toPandas().to_excel(writerGov,sheet_name =i)
    cityActive[i].toPandas().to_excel(writerActive,sheet_name =i)
    cityNight[i].toPandas().to_excel(writerNight,sheet_name =i)
    cityArts[i].toPandas().to_excel(writerArts,sheet_name =i)
    
