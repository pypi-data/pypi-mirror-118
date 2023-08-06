from typing import Dict, List, Any

from pyspark.sql import DataFrame, Row
import re

from pyspark.sql.types import *
import pyspark.sql.functions as f


def __rgm(col, *pattern: str) -> bool:
    if not pattern:
        return True
    for pat in pattern:
        expr = "^" + pat.replace("*", ".+").replace("^", "") + "$"
        if re.search(expr, col):
            return True
    return False


def bn_select(self: DataFrame, *pattern: str) -> DataFrame:
    cols = [c for c in self.columns if __rgm(c, *pattern)]
    return self.select(*cols)


def bn_drop(self: DataFrame, pattern: str = "*") -> DataFrame:
    expr = pattern.replace("*", ".+")
    cols = [c for c in self.columns if re.search(expr, c)]
    return self.select(*cols)


def bn_display(self: DataFrame, max_rows: 20) -> None:
    for column in self.schema:
        t = type(column.dataType)
        if t == StructType or t == ArrayType or t == MapType:
            self = self.withColumn(column.name, f.to_json(column.name))
    self.show(max_rows, truncate=False)


def bn_union(self: DataFrame, df2: DataFrame) -> DataFrame:
    # take first df and add missing columns, filling them with nulls
    df1u = self
    for df2c in df2.columns:
        if df2c not in self.columns:
            df1u = (df1u.withColumn(df2c, f.lit(None)))

    # take df2 and make it idential in order and columns to df1u
    cols2 = []
    for df1c in df1u.columns:
        if df1c in df2.columns:
            # add own column
            cols2.append(f.col(df1c))
        else:
            # add a dummy
            cols2.append(f.lit(None).alias(df1c))
    df2u = df2.select(*cols2)
    df = df1u.union(df2u)

    return df


def as_list_of_dict(self: DataFrame) -> List[Dict[str, Any]]:
    row_list: List[Row] = self.collect()
    return [r.asDict(True) for r in row_list]


def head_as_dict(self: DataFrame) -> Dict[str, Any]:
    r: Row = self.head()
    return r.asDict(True)


def col_as_list(self: DataFrame, col_name: str = None) -> List[Any]:
    df = self
    if col_name:
        df = df.select(col_name)
    rows = df.collect()
    return [x[0] for x in rows]


DataFrame.bn_select = bn_select
DataFrame.bn_drop = bn_drop
DataFrame.bn_display = bn_display
DataFrame.bn_union = bn_union
DataFrame.as_list_of_dict = as_list_of_dict
DataFrame.head_as_dict = head_as_dict
DataFrame.col_as_list = col_as_list
