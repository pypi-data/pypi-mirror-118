from pyspark.sql import SparkSession
from bigninja import *

spark = SparkSession.builder.config("spark.driver.host", "127.0.0.1").getOrCreate()

df1 = spark.createDataFrame([
    {
        "id": 1,
        "name": "Ivan"
    },
    {
        "id": 2,
        "name": "Unknown"
    }
])

df2 = spark.createDataFrame([
    {
        "id": 1,
        "city": "London"
    }
])

dfw = spark.createDataFrame([
    {
        "id1": 1,
        "id2": 11,
        "city1": "London",
        "city2": "London"
    }
])


def test_select_simple():
    df = dfw.bn_select("i*")
    assert ["id1", "id2"] == df.columns


def test_select_two():
    df = dfw.bn_select("i*", "ci", "ci*")
    assert ["city1", "city2", "id1", "id2"] == df.columns


def test_union():
    df: DataFrame = df1.bn_union(df2)
    assert ["id", "name", "city"] == df.columns
    assert 3 == df.count()
    assert df.head_as_dict() == {
        "id": 1,
        "name": "Ivan",
        "city": None
    }
