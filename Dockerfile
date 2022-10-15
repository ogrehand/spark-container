
# builder step used to download and configure spark environment
FROM openjdk:17.0.2-slim-buster as builder

# Add Dependencies for PySpark
RUN apt-get update &&\
    apt-get install -y curl vim wget software-properties-common ssh net-tools ca-certificates python3 python3-pip &&\
    pip3 install pyspark

RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1

# Fix the value of PYTHONHASHSEED
# Note: this is needed when you use Python 3.3 or greater
ENV SPARK_VERSION=3.3.0 \
HADOOP_VERSION=3 \
SPARK_HOME=/opt/spark/spark-3.3.0-bin-hadoop3

# Download and uncompress spark from the apache archive
RUN mkdir -p /opt/spark \
&& useradd -m spark

WORKDIR /opt/spark

COPY --chown=spark:spark spark-3.3.0-bin-hadoop3.tgz /opt/spark
COPY start-spark.sh /opt/spark

RUN tar zxvf spark-3.3.0-bin-hadoop3.tgz &&\
    rm -rf spark-3.3.0-bin-hadoop3.tgz

WORKDIR /opt/spark/spark-3.3.0-bin-hadoop3

# Apache spark environment
# FROM builder as apache-spark

ENV SPARK_MASTER_PORT=7077 \
SPARK_MASTER_WEBUI_PORT=8080 \
SPARK_LOG_DIR=/opt/spark/spark-3.3.0-bin-hadoop3/logs \
SPARK_MASTER_LOG=/opt/spark/spark-3.3.0-bin-hadoop3/logs/spark-master.out \
SPARK_WORKER_LOG=/opt/spark/spark-3.3.0-bin-hadoop3/logs/spark-worker.out \
SPARK_WORKER_WEBUI_PORT=8080 \
SPARK_WORKER_PORT=7000 \
SPARK_MASTER="spark://spark-master:7077" \
SPARK_WORKLOAD="master" \
SPARK_NO_DAEMONIZE=true


RUN mkdir -p $SPARK_LOG_DIR && \
touch $SPARK_MASTER_LOG && \
touch $SPARK_WORKER_LOG && \
ln -sf /dev/stdout $SPARK_MASTER_LOG && \
ln -sf /dev/stdout $SPARK_WORKER_LOG
