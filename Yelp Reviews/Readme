Analyzing Yelp Open Data to display the importance of the customer reviews based on Word Distribution in Spark using PySpark and SparkSQL

PROCESS

1) Environment Setup
The first and foremost requirement while performing this analysis was to set up the Hadoop environment correctly. We uploaded all of the dataset into the school cluster using SmarTTY,
and then transferred them to RDD.

2) Data Preparation
We only focus on yelp business dataset and yelp review dataset because we believed these two would cover all the operations above and be enough for the scope of our project. For review
data, we filtered any null values from the file. For business data, we took required columns and renamed column business and column star for future use. However, we still need a master
dataset which connects businesses and related reviews, so we merged business dataset and review dataset by “business id” and dropped several columns that are irrelevant to our scope of
work.

3) MapReduce
We found in the yelp business dataset, the column Category is very detailed with more than one thousand levels, which will distract our results. We applied MapReduce function to group
the original categories into main sectors according to the official category list:https://www.yelp.com/developers/documentation/v3/category_list.


Related Work
A lot of work is being done to make the useful and informative analysis of reviews available in Yelp Dataset. Among the many available kernels, we came across, we would like to highlight the
following works since they were the most relevant to our objective.

- https://www.kaggle.com/ambarish/a-very-extensive-data-analysis-of-yelp
- https://www.kaggle.com/niyamatalmass/finding-the-perfect-restaurants-on-yelp •
- https://www.kaggle.com/tibhar940/yelp-find-eda-fe-visualization-near-kaggle
