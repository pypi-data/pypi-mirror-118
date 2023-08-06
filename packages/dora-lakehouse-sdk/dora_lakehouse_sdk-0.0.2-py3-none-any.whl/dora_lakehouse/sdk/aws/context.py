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
import boto3
from os import environ
from botocore.errorfactory import ClientError
from dora_lakehouse.sdk import logger
from dora_lakehouse.sdk.catalog import Table
from dora_lakehouse.sdk.datatable import DataTable
from dora_lakehouse.sdk.context import Context as DoraContext

S3C = boto3.client('s3', region_name=environ.get("AWS_DEFAULT_REGION","us-east-1"))

class Context(DoraContext):
    """Dora lake house context for AWS"""

    @classmethod
    def from_path(cls, path):
        """Parser an path to bucket and prefix valures to S3"""
        _bucket = str(path).split('/')[2]
        _prefix = '/'.join(str(path).split('/')[3:])
        return [_bucket, _prefix]

    def upload_files(self, path:str, stage_files:list, table:Table) -> list:
        """Write master dataframe
        :param path: Path to files destination
        :param stage_files: list of files in stage area
        :return: list of files writen
        """
        _bkt, _pfx  = Context.from_path(path)
        for _file in stage_files:
            _key = f"""{_pfx}/{str(_file).split(f"/{table.database.name}/{table.name}/")[-1]}"""
            logger.debug("UPLOAD:FILE:%s:S3:%s:%s",_file,_bkt,_key)
            yield f"s3://{_bkt}/{_key}"
            S3C.upload_file(Filename=str(_file),Bucket=_bkt, Key=_key)

    def write_master(self, data_table:DataTable) -> list:
        """Write master dataframe
        :param data_table: Data table object
        :return: list of files writen
        """
        return list(
            self.upload_files(
                path=self._ods_path_(data_table.table, remote=True),
                stage_files=self.stage_master(data_table),
                table=data_table.table
                )
            )

    def write_refined(self, data_table:DataTable) -> list:
        """Write refined dataframe
        :param data_table: Data table object
        :return: list of files writen
        """
        return data_table.table.update_partitions(
            self.upload_files(
                path=self._rfn_path_(data_table.table, remote=True),
                stage_files=self.stage_refined(data_table),
                table=data_table.table))

    def exists(self,path) -> bool:
        """Implement this method to check if an file exists
        :param path: full path to file
        :return: True if exists
        """
        _bkt, _pfx = Context.from_path(path)
        try:
            results = S3C.head_object(Bucket=_bkt, Key=_pfx)
            logger.debug("EXISTS:%s",results)
        except ClientError:
            logger.debug("NOTEXISTS:%s",path)
            return False
        return True
