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
"""Lakehouse Glue Catalog"""
import json
import re
from os import environ
import boto3
from botocore.exceptions import ClientError
from dora_lakehouse.sdk.catalog import Database as AbstractDatabase
from dora_lakehouse.sdk.catalog import Column as AbstractColumn
from dora_lakehouse.sdk.catalog import Table as AbstractTable
from dora_lakehouse.sdk import sanitize, logger

GLUE = boto3.client('glue')

class Database(AbstractDatabase):
    """Glue database definition"""
    @classmethod
    def load(cls, name:str):
        """Load database from Glue Catalog
        :param name: Database name
        :return: Database object
        """
        response = GLUE.get_database(Name=sanitize(name))['Database']
        return Database(
            name=response['Name'],
            description=response.get('Description'),
            location=response.get('LocationUri'),
            parameters=response.get('Parameters'))

    def representation(self) -> dict:
        """Glue Database representation, compatible with API
        :return: Dictionary Representation, compatible with API"""
        response = dict(Name=self.name)
        if self.description is not None:
            response['Description'] = self.description
        if self.location is not None:
            response['LocationUri'] = self.location
        if len(self.parameters)>0:
            response['Parameters'] = self.parameters
        return response

    def save(self) -> bool:
        """Save the database definition
        :return: True if the object was success persisted"""
        try:
            response = GLUE.create_database(
                DatabaseInput=dict(self))
            logger.info("Database Created: %s", response)
        except ClientError as err:
            logger.debug("%s", err)
            response = GLUE.update_database(
                Name=self.name,
                DatabaseInput=dict(self))
            logger.info("Database Updated: %s", response)
        return True

class Column(AbstractColumn):
    """Glue column definition"""
    @classmethod
    def load(cls, col:dict, partition=False):
        """Init column object based on Glue configuration"""
        params = dict(
            name=col['Name'],
            data_type=col['Type'],
            partition=partition,
            description=col.get('Comment'))
        if col.get('Parameters'):
            if col['Parameters'].get('index') is not None:
                params['index']=bool(col['Parameters']['index'])
            if col['Parameters'].get('tiebreake'):
                order, function = col['Parameters']['tiebreake'].split(',')
                params['tiebreaker']=(order, function)
        return Column(**params)

    def representation(self) -> dict:
        """Glue Column representation, compatible with API
        :return: Dictionary Representation, compatible with API"""
        response = dict(
            Name=self.name,
            Type=self.data_type)
        if self.description is not None:
            response["Comment"]=self.description
        prm = dict()
        if self.isindex():
            prm['index']=str(self.index)
        if self.istiebreaker():
            prm['tiebreake']=f"{self.tiebreak[0]},{self.tiebreak[1]}"
        if len(prm)>0:
            response["Parameters"]=prm
        return response

class Table(AbstractTable):
    """Glue Table definition"""
    @classmethod
    def load(cls, database:Database, name:str):
        """Load table definition from AWS Glue Catalog
        :param database: Database Object
        :param name: Table name
        :return: Table object
        """
        response = GLUE.get_table(DatabaseName=database.name,Name=name)['Table']
        logger.debug(response)
        _cols = [Column.load(col) for col in response['StorageDescriptor']['Columns']]
        pks_parms = response['Parameters'].get('PartitionKeys')
        if pks_parms is not None:
            pks_parms = json.loads(pks_parms.replace("'",'"'))
        for _col in response['PartitionKeys']:
            try:
                _col['Parameters']=pks_parms[_col['Name']]
            except KeyError:
                pass
            _cols.append(Column.load(_col, partition=True))
        src = response['Parameters'].get('Source')
        if src is not None:
            src = json.loads(src.replace("'",'"'))
        return Table( 
            database = database, 
            name = name,
            location = response['StorageDescriptor']['Location'],
            columns = _cols,
            hash_def=response['Parameters']['Hash'],
            source=src,
            check=response['Parameters'].get('Check'),
            description=response.get('Description'),
            table_type=response['TableType'],
            serialization=response['StorageDescriptor']['Parameters'].get('classification'),
            compression=response['StorageDescriptor']['Parameters'].get('compressionType','uncompressed'),
            serde_library=response['StorageDescriptor']['SerdeInfo']['SerializationLibrary'],
            serde_input=response['StorageDescriptor']['InputFormat'],
            serde_output=response['StorageDescriptor']['OutputFormat'])
    
    def representation(self) -> dict:
        """Glue Table representation, compatible with API
        :return: Dictionary Representation, compatible with API"""
        # Storae Descriptor
        stg = dict(
            Columns=[dict(col) for col in self.datacolumns],
            Location=self.location,
            InputFormat=self.serde_input,
            OutputFormat=self.serde_output,
            SerdeInfo=dict(SerializationLibrary=self.serde_library),
            Parameters=dict(classification=self.serialization))
        # Compression information
        if self.compression != 'uncompressed':
            stg['Compressed']=True
            stg['Parameters']['compressionType']=self.compression
        # Main info
        response = dict(
            Name=self.name,
            TableType=self.table_type,
            Parameters=dict(
                Hash=self.hash_def,
                Check=self.checksum()),
            StorageDescriptor=stg)
        if self.source is not None:
            response['Parameters']['Source'] = str(self.source)
        if self.description is not None:
            response['Description'] = self.description
        partition_keys = list()
        partition_para = dict()
        for pks in [dict(ptk) for ptk in self.partitions]:
            try:
                partition_para[pks['Name']]=pks.pop('Parameters')
            except KeyError:
                pass
            partition_keys.append(pks)
        if len(partition_keys) > 0:
            response['PartitionKeys'] = partition_keys
        if len(partition_para) > 0:
            response['Parameters']['PartitionKeys'] = str(partition_para)
        return response

    def repair_partitions(self) -> bool:
        """Uses Athena MSCK REPAIR TABLE command scans a file system such as Amazon S3 for Hive compatible partitions that were added to the file system after the table was created"""
        return boto3.client('athena').start_query_execution(
            QueryString=f'MSCK REPAIR TABLE {self.full_name}',
            QueryExecutionContext={'Database': self.database.name},
            ResultConfiguration={'OutputLocation': environ['BKT_STG']}
        )['ResponseMetadata']['HTTPStatusCode']==200

    def update_partitions(self, files:list):
        """Update partitions on catalog
        :param files: list of files to register partitions
        """
        regex = r"\/([%@#$&*+A-Z0-9_-]+)=([%@#$&*+A-Z0-9_-]+)"
        paths = set()
        for file in files: # Filter
            paths.add('/'.join(file.split('/')[:-1]))
        storage_description = self.representation().get('StorageDescriptor')
        partition_names = [_pt.name for _pt in self.partitions]
        for path in paths:
            values = [match.group(2) for match in re.finditer(regex, path, re.IGNORECASE) if match.group(1) in partition_names]
            if len(values)==0:
                logger.debug('UPDATE:TABLE:PARTITION:Config not found')
                continue
            try:
                storage_description['Location']=path
                response = GLUE.create_partition(
                    DatabaseName =self.database.name,
                    TableName = self.name,
                    PartitionInput = {
                        'Values': values,
                        'StorageDescriptor':storage_description})
                logger.debug('UPDATE:TABLE:PARTITION:%s', response)
            except ClientError as err:
                if err.response['Error']['Code']=='AlreadyExistsException':
                    logger.debug(err)
                    continue
                else:
                    raise err
        return files

    def save(self) -> bool:
        """Save definition in the Data Catalog
        :return: True if the object was success persisted
        """
        try: #Check if the database exists
            Database.load(self.database.name)
        except ClientError as err: #if not
            logger.warning(err) # warn about
            self.database.save() # and create
        try: # Try to save table
            response = GLUE.get_table(DatabaseName=self.database.name,Name=self.name)['Table']
            self.check = response['Parameters'].get('Check')
            if self.ischanged:
                logger.info("Update table '%s'", self.full_name)
                response = GLUE.update_table(
                    DatabaseName=self.database.name,
                    TableInput=dict(self))
                logger.debug(response)
                return self.repair_partitions()
            logger.debug("Table '%s' not change", self.full_name)
            return True
        except ClientError as err:
            logger.info("Create table '%s'", self.full_name)
            response = GLUE.create_table(
                DatabaseName=self.database.name,
                TableInput=dict(self))
            logger.debug(response)
            return True
        raise ValueError("Cant save table on Glue")
