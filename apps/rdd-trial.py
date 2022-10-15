from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName('testRDD').setMaster("spark://6a125a083996:7077")
sc = SparkContext(conf=conf)

data = [1, 2, 3, 4, 5]
distData = sc.parallelize(data)

rdd = sc.parallelize(range(1, 10000)).map(lambda x: (x, "a" * x))
rdd.saveAsSequenceFile("/opt/spark-data/hasil")
sorted(sc.sequenceFile("/opt/spark-data/hasil").collect())