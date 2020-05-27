"""
This script takes the initial passim outputs (pairwise or aggregated before) and adds character match (without counting
white spaces), char match percentage (using length of the aligned string), and word match to each alignment.
The output files will have the same structure as the passim outputs with four new columns:
    ch_match: character match without counting white spaces,
    align_len: length of the aligned string to be used in percentage value,
    matches_percentage: character match percentage using passim column "matches", which counts white spaces in
    char match, and 'align_len' column, which we produce above,
    w_match: word match
"""

from __future__ import print_function
import sys

from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as F


def word_count(s1, s2):
    cnt = 0
    i = 0
    while i < len(s1):
        # print("i: ", i)
        prev_i = i
        while i < len(s1) and s1[i] != " ":
            i += 1
        if s1[prev_i:i] == s2[prev_i:i]:
            cnt += 1
        i += 1
    return cnt


def ch_count(s1, s2):
    cnt = 0
    for i in range(0, len(s1)):
        if s1[i] == s2[i] and all(s != " " for s in [s1[i], s2[i]]):
            cnt += 1
    return cnt


def match_per(match, length):
    if length == 0:
        return 0
    else:
        return (match/length) * 100


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: align-stats_CM-WM.py <input> <output>", file=sys.stderr)
        exit(-1)
    # spark session
    spark = SparkSession.builder.appName('Stats').getOrCreate()

    word_match = F.udf(lambda s1, s2: word_count(s1, s2), IntegerType())
    ch_match = F.udf(lambda s1, s2: ch_count(s1, s2), IntegerType())
    match_percent = F.udf(lambda match, alig_len: match_per(match, alig_len), FloatType())
    align_len = F.udf(lambda s: len(s), IntegerType())

    # check the input format whether it is JSON or parquet
    in_file = sys.argv[1]
    if in_file.strip("/").endswith(".json"):
        file_type = "json"
    elif in_file.strip("/").endswith(".parquet"):
        file_type = "parquet"

    # define the matches_percent column
    ch_match_percent_col = F.when(F.col("align_len") == 0, 0.0)\
        .otherwise(match_percent('matches', 'align_len'))

    df = spark.read.format(file_type).options(encoding='UTF-8').load(in_file)
    dfGrouped = df.withColumn('ch_match', ch_match('s1', 's2')) \
        .withColumn('align_len', align_len('s1')) \
        .withColumn('matches_percent', ch_match_percent_col) \
        .withColumn('w_match', word_match('s1', 's2')) \
        .repartition('series1') \
        .sortWithinPartitions('series2') \
        .write \
        .format('json') \
        .options(header='true') \
        .save(sys.argv[2])

    spark.stop()
