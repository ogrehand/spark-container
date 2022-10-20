from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, size, concat, lit
import requests


def check_robots(url):
    file = requests.get("https://"+url['value']+"/robots.txt")
    with open(f'/opt/spark-data/robots/robot_{url["value"]}.txt','wb') as f:
        f.write(file.content)
    

spark = SparkSession \
    .builder \
    .master("spark://0b8e871de997:7077") \
    .appName("Python robots.txt scrapper") \
    .getOrCreate()


links = spark.read.text("/opt/spark-data/link-robot.txt")
links.show()

links_rdd = links.rdd
links_rdd.foreach(check_robots)
# links_rdd.collect()