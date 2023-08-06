# -*- coding: utf-8 -*-
#
# Copyright 2021 Compasso UOL
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Lakehouse Context"""
import datetime
import hashlib
import os
import re
import shutil
import time
from abc import ABC, abstractmethod
from pathlib import Path
from pyspark.sql.context import SQLContext
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import col as spark_col
from pyspark.sql.functions import concat_ws
from pyspark.sql.functions import expr as spark_expr
from pyspark.sql.functions import lit as spark_lit
from pyspark.sql.types import StructField, StringType, BooleanType

from dora_lakehouse.sdk import logger
from dora_lakehouse.sdk.catalog import Table
from dora_lakehouse.sdk.datatable import DataTable
from dora_lakehouse.sdk.datatable import HASH_COL
from dora_lakehouse.sdk.datatable import IDX_COL
from dora_lakehouse.sdk.datatable import NAME_SIZE
from dora_lakehouse.sdk.datatable import DEL_COL

MD5 = lambda value: hashlib.md5(str(value).encode('utf-8')).hexdigest()

def clean_file_system(path:str, temporary=False, hours:int=0) -> list:
    """Remove all files in a directory
    :param path: root directory
    :param hours: keep files with less then this parameter: Default 0 to remove all
    """
    partitions = set()
    dir_to_search = Path(path)
    for dirpath, directories, filenames in os.walk(dir_to_search):
        for _dir in directories:
            if f"{HASH_COL}=" in _dir:
                partitions.add(_dir.split(f"{HASH_COL}=")[1])
        try:
            if len(filenames)==0:
                continue
            for _file in filenames:
                curpath = os.path.join(dirpath, _file)
                if temporary:
                    if _file.startswith('_') or _file.startswith('.') :
                        os.remove(curpath)
                    continue
                file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
                if datetime.datetime.now() - file_modified > datetime.timedelta(hours=int(hours)):
                    os.remove(curpath)
                    logger.debug(curpath)
            os.rmdir(dirpath)
        except OSError:
            continue
    return list(partitions)

class Context(SQLContext, ABC):
    """Dora Lakehouse Context Object"""
    SHAREDFS = os.environ['SHAREDFS']
    METADIR = f"{SHAREDFS}/meta/"
    BKT_STG= os.environ['BKT_STG'] # Full path to stage bucket
    BKT_ODS= os.environ['BKT_ODS'] # Full path to ods bucket
    BKT_RFN= os.environ['BKT_RFN'] # Full path to refined bucket
    CACHE = os.environ.get('CACHE',"Y")
    WRITE_MODES = ['overwrite','append']
    TOPIC = lambda table: f"""{table.database.name}/{table.name}"""

    @classmethod
    def _update_sequence_(cls, dirpath:Path, increment) -> int:
        """Update table sequence"""
        seq_file = os.path.join(dirpath, "sequence")
        Path(seq_file).touch() # Create file if not exists
        with open(seq_file, 'r') as reader:
            try:
                value = int(reader.read())
            except ValueError:
                value = 0
                logger.info("SEQUENCE:CREATED")
            finally:
                if increment > 0:
                    with open(seq_file, 'w') as writer:
                        writer.write(str(increment+value))
            logger.info("SEQUENCE:VALUE:%s",value)
            return value

    @classmethod
    def _sequence_(cls, table:Table, increment:int=-1, attempts:int=10) -> int:
        """Get and update table sequence metadata
        :param table: table where the sequence will be apply
        :param increment: sequence increment to update, if greater then 0.
        :param attempts: max number of attempts to get the sequence value
        :return: sequence value before update
        """
        dirpath = Path(f"{cls.METADIR}/{cls.TOPIC(table)}")
        lock = os.path.join(dirpath, ".lock")
        for attempt in range(attempts):
            try:
                os.makedirs(lock, exist_ok=False)
                logger.debug("SEQUENCE:LOCK:%s",lock)
                try:
                    return cls._update_sequence_(dirpath, increment)
                finally:
                    os.rmdir(lock)
                    logger.debug("SEQUENCE:UNLOCK:%s",lock)
            except FileExistsError:
                logger.debug("SEQUENCE:ATTEMPT:%s",attempt)
                time.sleep(1)
        raise ValueError(f"Sequece Unreachable after {attempts} attempts")

    @classmethod
    def _group_names_(cls, names:list, regex:str=r"(max|min)\((.+)\)"):
        """ After using agregation functions Spark change the column original name
        This function receives the list of names and by regular expression get the original column name
        :param names: data frame column names
        :param regex: regular expression
        :return: list of names
        """
        for _col in names:
            try:
                match = re.finditer(regex, _col, re.IGNORECASE)
                yield next(match).group(2)
            except StopIteration:
                yield _col

    @classmethod
    def _filter_(cls, rdf:DataFrame, table:Table) -> DataFrame:
        """Filter dataframe by table definitions"""
        # Name of all columns used to filter
        att = [i.name for i in table.indexes]
        # If the data frame has no index
        if len(att)==0:
            return rdf.dropDuplicates()
        # Create an dataframe grouped by index to filter the original by tiebreacks
        gdf = rdf.where('1=1')
        for tbk in table.tiebreaks:
            gdf = gdf.groupBy(att).agg({tbk.name:tbk.tiebreak[1]})
            gdf = gdf.toDF(*Context._group_names_(gdf.columns))
            att.append(tbk.name)
            # Create the WHERE clausule
            whr = [rdf[att[i]]==gdf[att[i]] for i in range(len(att))]
            # Filter by tiebreack dataframe
            fdf = rdf.join(gdf,on=whr,how='inner')
            gdf = fdf.select([rdf[c] for c in rdf.columns])
        return gdf.dropDuplicates()

    @classmethod
    def _indexing_(cls, rdf:DataFrame, table:Table) -> DataFrame:
        """Apply index to the dataframe"""
        if table.indexes is None or table.update == 'append':
            function = f"(row_number() OVER (PARTITION BY 1 ORDER BY 1))+{Context._sequence_(table,rdf.count())}"
            logger.debug("SEQUENCE:%s",function)
            return rdf.withColumn(IDX_COL, spark_expr(function))
        idx = [spark_col(i.name) for i in table.indexes]
        return rdf.withColumn(IDX_COL, concat_ws('-', *idx))

    @classmethod
    def _hashing_(cls, rdf:DataFrame, table:Table) -> DataFrame:
        """Apply hash data function"""
        if table.hash_def is None:
            raise ValueError('Cant find data hash function')
        hash_function = f"lpad(abs(ceil({table.hash_def})),{NAME_SIZE},'0')"
        logger.debug("DATA:HASH:%s",hash_function)
        return rdf.withColumn(HASH_COL, spark_expr(hash_function))

    @abstractmethod
    def exists(self,path) -> bool:
        """Implement this method to check if an file exists in the Data Lake file storage system
        :param path: full path to file
        :return: True if exists
        """

    @abstractmethod
    def write_master(self, data_table:DataTable) -> list:
        """Write master dataframe
        :param data_table: Data table object
        :return: list of files writen
        """

    @abstractmethod
    def write_refined(self, data_table:DataTable) -> list:
        """Write refined dataframe
        :param data_table: Data table object
        :return: list of files writen
        """

    def __init__(self, spark, identifier:str=None):
        """Create Context
        :param spark: Context from spark driver
        :param identifier: Context identifier, if null uses Spark app ID
        """
        super().__init__(spark.sparkContext, spark)
        self.identifier = MD5(identifier)
        self.spark_context = spark.sparkContext
        self.cache = Context.CACHE=='Y'
        if identifier is None:
            self.identifier = MD5(spark.conf.get('spark.app.id'))

    def _stg_path_(self, table:Table, prefix:str='stg', proc:bool=True, remote=False) -> str:
        """Stage Path local path
        :param table: Table object
        :return: Local path to stage directory
        """
        _path = f"{Context.SHAREDFS}/{prefix}/{Context.TOPIC(table)}"
        if remote:
            _path = f"{Context.BKT_STG}/{Context.TOPIC(table)}"
        if proc:
            return f"{_path}/proc={self.identifier}"
        return str(_path)
    
    def _ods_path_(self, table:Table, prefix:str='ods', remote=False) -> str:
        """Operational data store local path
        :param table: Table object
        :return: Local path to ODS directory
        """
        if remote:
            return f"{Context.BKT_ODS}/{Context.TOPIC(table)}"
        return str(Path(f"{Context.SHAREDFS}/{prefix}/{Context.TOPIC(table)}"))

    def _rfn_path_(self, table:Table, prefix:str='rfn', remote=False) -> str:
        """Refined data local path
        :param table: Table object
        :return: Local path to Refined directory
        """
        if remote:
            return table.location
        return str(Path(f"{Context.SHAREDFS}/{prefix}/{Context.TOPIC(table)}"))

    def from_stage(self, hash_id:str, table:Table) -> DataTable:
        """Read data table from stage by hash key
        :param hash_id: hash key, indicates who file will be loaded
        :param table: table definition
        :return: Data Table object"""
        self.clearCache()
        path = f"{self._stg_path_(table,proc=False)}/*/{HASH_COL}={hash_id}/*"
        logger.debug("READING:STAGE:%s:%s", hash_id, path)
        return self.from_data_frame(
            self.read.format('avro').load(path).dropDuplicates(), table)

    def stage_master(self, data_table:DataTable, update:bool=True):
        """Persist master data frame on stage directory"""
        path = self._ods_path_(data_table.table, ".ods")
        if update:
            logger.debug("UPDATE:WITH:MASTER")
            data_table.update()
        logger.debug("WRITE:MASTER:STAGE")
        data_table.orderBy(data_table.keys)\
            .repartition(1, HASH_COL)\
            .write.partitionBy(HASH_COL)\
            .mode("overwrite")\
            .format("avro")\
            .options(**{"compression":"snappy"})\
            .save(str(path))
        logger.debug("MOVE:MASTER:STAGE")
        return self._move_(
            path_from=path,
            path_to=self._ods_path_(data_table.table),
            file_type="avro")

    @classmethod
    def partition_values(cls, files, table, regex:str=r"(.+)=(.+)"):
        """Search for partition values based on staged files"""
        partitions = {_pt.name:set() for _pt in table.partitions}
        for file in files:
            for token in str(file).split('/'):
                try:
                    metch = next(re.finditer(regex, token))
                    if metch.group(1) in partitions.keys():
                        partitions[metch.group(1)].add(metch.group(2))
                except StopIteration:
                    continue
        return partitions

    def stage_refined(self, data_table:DataTable, master:bool=True):
        """Persist master data frame on stage directory"""
        if master:
            logger.debug("WRITE:MASTER")
            master_files = self.write_master(data_table)
            logger.debug("UPDATE:MASTER:LAKE:%s", master_files)
        path = self._rfn_path_(data_table.table, ".rfn")
        logger.debug("WRITE:REFINED:STAGE:%s", path)
        data_table.filter(f"{DEL_COL} is false")\
            .orderBy(data_table.keys)\
            .repartition(1, HASH_COL)\
            .write.partitionBy([HASH_COL]+[_par.name for _par in data_table.table.partitions])\
            .mode("overwrite")\
            .format("parquet")\
            .options(**{"compression":"snappy"})\
            .save(str(path))
        logger.debug("MOVE:REFINED:STAGE:%s", path)
        return self._move_(
            path_from=path,
            path_to=self._rfn_path_(data_table.table),
            file_type="parquet")

    def _master_files_(self, table:Table, hashs:list) -> list:
        """Find all files needed to load master data"""
        for key in hashs: # For each hash key
            remote_path = f"{self._ods_path_(table, remote=True)}/{key}.avro"
            local_path = f"{self._ods_path_(table, remote=False)}/{key}.avro"
            if self.cache and os.path.exists(local_path):
                logger.debug("LOAD:%s",local_path)
                yield local_path
            elif self.exists(remote_path):
                logger.debug("LOAD:%s",remote_path)
                yield remote_path
            else:
                logger.warning('MASTER:%s:Not found',key)

    def load_master(self, hashs:list, table:Table) -> DataTable:
        """Read data table from stage by hash key
        :param hashs: list of hash keys, indicates who files will be loaded
        :param table: table definition
        :return: Data Table object"""
        self.clearCache()
        files = list(self._master_files_(table,hashs))
        if len(files)>0:
            return DataTable(self, self.read.format('avro').load(files), table)
        # If this keys dont exists, return an empty data table
        _schema = table.schema\
            .add(StructField(IDX_COL, StringType(), False))\
            .add(StructField(DEL_COL, BooleanType(), False))\
            .add(StructField(HASH_COL, StringType(), True))
        return DataTable(self, self.createDataFrame(self.spark_context.emptyRDD(), _schema), table)

    def from_data_frame(self, data_frame:DataFrame, table:Table) -> DataTable:
        """Create am table data object
        :param data_frame: Pyspark Dataframe object
        :param table: Table object representation
        :return: Data Table object"""
        # Equalize the columns by table definition
        _rdd = DataTable.schema_equalization(data_frame, table).rdd
        # Filter data by tiebreaks
        schema = table.schema
        for _pc in DataTable.PSEUDO_COLUMNS:
            schema.add(_pc.field)
        _df = Context._filter_(self.createDataFrame(_rdd, schema),table)
        # Create the table index an ordered the data
        _df = Context._indexing_(_df,table)
        # Mark the deleted values
        #TODO:Create an process to anonimization when the row is marked as deleted
        _df = _df.withColumn(DEL_COL, spark_expr(f"ifnull(({table.delete}),False)"))
        # Create hash column
        _df = Context._hashing_(_df,table)
        # Order by columns in 'order'
        return DataTable(self, _df, table)

    def _walk_(self, path:Path, file_type:str):
        """Walk into directory and recovery the file names"""
        for dirpath, dirnames, filenames in os.walk(path):
            for dirname in dirnames:
                filenames.append(self._walk_(os.path.join(dirpath, dirname),file_type))
            for filename in filenames:
                if str(filename).endswith(file_type): # If are an valid file
                    yield os.path.join(dirpath, filename)

    def _move_(self, path_from:str, path_to:str, file_type:str):
        """Move files to new layer
        :param path: directory where the files are current stored
        :param layer: destination directory
        :return: list of files moved"""
        if file_type=='parquet': # Clean refined layer, only rfn uses parquet format
            shutil.rmtree(path_to, ignore_errors=True)
        # For each key, move and rename files
        for hash_key in clean_file_system(path_from, temporary=True):
            dir_to_search=Path(f"{path_from}/{HASH_COL}={hash_key}")
            for _file in self._walk_(dir_to_search, file_type):
                dest_dir = '/'.join(str(_file).replace(str(dir_to_search),str(path_to)).split('/')[:-1])
                destiny = Path(f"{dest_dir}/{hash_key}.{file_type}")
                logger.debug("MOVE:%s:TO:%s", _file, destiny)
                os.makedirs(dest_dir, exist_ok=True)
                yield shutil.move(_file, destiny)
            # Clean directory
            shutil.rmtree(dir_to_search, ignore_errors=True)
        shutil.rmtree(path_from, ignore_errors=True)

    def write_stage(self, data_table:DataTable):
        """Persist data frame on stage directory"""
        path = self._stg_path_(data_table.table)
        data_table.write.partitionBy(HASH_COL)\
            .mode("append")\
            .format("avro")\
            .options(**{"compression":"snappy"})\
            .save(path)
        data_table.hash_list = clean_file_system(path, temporary=True)
        return data_table.hashs
