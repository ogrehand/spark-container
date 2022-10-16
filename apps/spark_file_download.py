from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, size, concat, lit
import requests


def download_file(url: str) ->None :
    print("nama mantan")
    print(url['value'])
    print(url['file_name'])
    file = requests.get(url['value'])
    with open(f'/opt/spark-data/file/{url["file_name"]}','wb') as f:
        f.write(file.content)


spark = SparkSession \
    .builder \
    .master("spark://bfb71c2164a3:7077") \
    .appName("Python Spark SQL basic example") \
    .getOrCreate()


links = spark.read.text("/opt/spark-data/link.txt")
splitted = split(links['value'],'/')
links = links.withColumn("file_name", concat(splitted[size(splitted)-1],lit('.csv')))
links.show()

links_rdd = links.rdd
print(links_rdd.count())
print(links_rdd.take(1))
print(links_rdd.foreach(download_file))
# links_rdd.collect()