from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName('first spark').setMaster("spark://6a125a083996:7077")
sc = SparkContext(conf=conf)


df = sc.read \
    .parquet("/opt/spark-data/yellow_tripdata_2021-01.parquet")
# Displays the content of the DataFrame to stdout
# df.show()
# print(df.columns)
# print(df.dtypes)
df.printSchema()

print(df.dtypes)
df_rdd = df.rdd
print(type(df_rdd))
print(df_rdd.count())
print(df_rdd.take(1))
print(df_rdd.filter(lambda x: x['PULocationID'] > 1).count())
counter =0
def increment_counter(x):
    global counter
    counter += 1
df_rdd.foreach(increment_counter)