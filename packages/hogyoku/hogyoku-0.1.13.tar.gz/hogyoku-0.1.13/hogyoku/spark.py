import datetime
import time
import re
import pyspark.sql.functions as fn
from pyspark.sql.types import *
from pyspark.sql import Window, DataFrame, Row
from pyspark.sql.functions import expr as SQL
import logging
from hogyoku.code import Courier, Code, bash

class SparkCacheNotRegistException(Exception):
    def __init__(self):
        super().__init__()

def filename_to_membername(filename):
    member_name = "_file_content_"+filename.split("/")[-1].replace(".", "_")
    member_name = f"_file_content_{re.sub('[^a-zA-Z0-9]', '_', filename)}"
    return member_name

class SparkCache(object):
    cache = None
    job = None
    hdfs_prefix = None
    registed = False
    dump = False
    input_dfs = []
    code = None
    debug = False
    spark = None
    url = None
    dt = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(days=2), '%Y-%m-%d')
    def __init__(self):
        assert self.registed, "You must run SparkCache.regist([job], [hdfs_prefix]) first!!"
    

    def set_file_content(self, filename):
        file_content = self.code(filename)
        member_name = filename_to_membername(filename)
        setattr(self, member_name, file_content)
    
    def get_file_content(self, filename):
        member_name = filename_to_membername(filename)
        if not hasattr(self, member_name):
            return None
        else:
            return getattr(self, member_name)

    def enable_global_dump(cls): cls.dump = True
    def disable_global_dump(cls): cls.dump = False

    def enable_debug(self): self.debug = True
    def disable_debug(self): self.debug = False

    def init_code(self, url):
        self.code = Code(url=url)

    @classmethod
    def regist(cls, spark, job, hdfs_prefix, url=None, filenames=[]):
        cls.spark = spark
        cls.job = job
        cls.hdfs_prefix = hdfs_prefix
        cls.registed = True
        cls.cache = SparkCache()
        cls.dep_map = dict()
        if url:
            cls.cache.init_code(url)
            for filename in filenames:
                cls.cache.set_file_content(filename)
            # globals()['cache'] = cls.cache

    def sample_if_debug(self, df, field, rate=0.01):
        m = 1_000_000
        n = int(m * rate)
        if self.debug:
            df = df.where(f"""
                int(substr(conv(substr(sha(cast({field} as string)), -8), 16, 10), -6)) % {m} <= {n}
            """)
        return df

    @classmethod
    def get_input_dfs(cls):
        return cls.input_dfs
    
    @classmethod
    def set_input_dfs(cls, dfs):
        cls.input_dfs.clear()
        for df in dfs:
            cls.input_dfs.append(df)

    def hdfspath(self, field):
        return f"{self.hdfs_prefix}/{self.job}/{field}/{self.dt}"
    
    def set(self, field, df):
        assert isinstance(df, DataFrame), "set a non-DataFrame object to cache"
        name = f"df_{field}"
        df = df.cache()
        setattr(self, name, df)
    
    def has(self, field):
        name = f"df_{field}"
        if hasattr(self.cache, name) and isinstance(self.get(field), DataFrame):
            return True
        return False

    def get(self, field):
        name = f"df_{field}"
        assert hasattr(self, name)
        df = getattr(self, name)
        return df

    def dumphdfs(self, field):
        df = self.get(field)
        if df.rdd.isEmpty():
            return False
        df.write.format("orc").mode("overwrite").save(self.hdfspath(field))
        return True
    
    def loadhdfs(self, field):
        if self.has(field):
            return self.get(field)
        df = self.spark.read.format("orc").load(self.hdfspath(field))
        return df
    
    def clear(self):
        for key, val in self.__dict__.items():
            if key.startswith("df_"):
                delattr(self, key)
        self.dep_map.clear()

def singleton_cache():
    return SparkCache.cache

def union_all(dfs):
    def algin_columns(df, colnames):
        cols = []
        exit_colnames = []
        for colname in colnames:
            if colname in df.columns:
                exit_colnames.append(colname)
                cols.append(SQL(f"{colname}"))
            else:
                cols.append(SQL(f"NULL as {colname}"))
        df = df.select(cols)
        return df

    assert len(dfs)>1, "len(dfs) > 1"
    colnames = []
    for df in dfs:
        colnames.extend(df.columns)
    colnames = list(set(colnames))
    for i in range(len(dfs)):
        dfs[i] = algin_columns(dfs[i], colnames)
    df_r = None
    for df in dfs:
        df_r = df if not df_r else df_r.unionByName(df)
    return df_r

def groupby_to_units(df, groupby_keys):
    struct_field_cols = [
        df[_].alias(_) for _ in df.columns if _ not in groupby_keys
    ]
    df = df.withColumn("unit", fn.struct(struct_field_cols))
    df = df.groupBy(*groupby_keys).agg(fn.collect_list("unit").alias('units'))
    return df

def merge_units(df, units_colname='units', output_unit_colname='unit'):
    returnType = df.schema[units_colname].dataType.elementType
    
    def _merge_units(unit_jsons):
        total_data = dict()
        for unit_json in unit_jsons:
            for field, val in unit_json.asDict().items():
                if val:
                    total_data[field] = val
        return total_data
    
    df = df.withColumn(output_unit_colname, fn.udf(_merge_units, returnType)(units_colname)) \
    .drop(units_colname)
    return df

def describe_unit(df, unit_colname='unit'):
    groupby_field_names = []
    for field_name in df.schema['unit'].dataType.fieldNames():
        groupby_field_name = f"unit_has_{field_name}"
        df = df.withColumn(groupby_field_name, 
                           SQL(f"{unit_colname}.{field_name} is not null").cast(IntegerType()))
        groupby_field_names.append(groupby_field_name)
    df.groupBy(groupby_field_names).count() \
    .orderBy("count", ascending=False).show()
    return df


def spark_step(out, deps=[], dump=False, verbose=True, joinkeys=[], join_sample_rate=1.,
        join_where_sql=None):
    #TODO enable join_sample_rate and join_where_sql
    class SparkStep(object):
        def __init__(self, func):
            self.out = out
            self.deps = deps
            self.dump = dump
            self.verbose = verbose
            self.func = func
            singleton_cache().dep_map[self.out] = self
        def __call__(self):
            cache = singleton_cache()
            for dep in self.deps:
                if not cache.has(dep):
                    try:
                        df_dep = cache.loadhdfs(dep)
                    except:
                        pass
                    else:
                        cache.set(dep, df_dep)
                if not cache.has(dep):
                    assert dep in cache.dep_map, f"no step will output {dep}"
                    dep_step = cache.dep_map[dep]
                    dep_step()
                    assert cache.has(dep), f"{dep} not ready after run {dep_step.__name__}"
            
            if joinkeys:
                dfs = [cache.get(dep) for dep in deps]
                df = union_all(dfs)
                df = groupby_to_units(df, joinkeys)
                df = merge_units(df)
                df = describe_unit(df)
                df = df.repartition(100)
                cache.set_input_dfs([df])
            else:
                cache.set_input_dfs([cache.get(dep) for dep in self.deps])
                    
            df_out = self.func()

            assert isinstance(df_out, DataFrame), "func return is not DataFrame"
            cache.set(self.out, df_out)

            if cache.dump or self.dump:
                if cache.dumphdfs(self.out) and self.verbose:
                    print(f"dump hdfs path = {cache.hdfspath(self.out)}")
            if self.verbose:
                count = df_out.count()
                print(f"df_{self.out}.count() = {count:,}")
                df_out.printSchema()
                df_out.show()
            return df_out
    return SparkStep
