"""
Copyright (C) 2021 Kaskada Inc. All rights reserved.

This package cannot be used, copied or distributed without the express 
written permission of Kaskada Inc.

For licensing inquiries, please contact us at info@kaskada.com.
"""

from kaskada.client import Client
import kaskada
import kaskada.staging as ks
import kaskada.api.v1alpha.table_pb2 as table_pb
import kaskada.api.v1alpha.staged_file_pb2 as staged_pb

import datetime
import grpc
import io
import os
import pandas as pd
import random
import requests
import tempfile


def list_tables(**kwargs):
    """
    Lists all the tables
    """
    try:
        client = kwargs.pop('client', kaskada.KASKADA_DEFAULT_CLIENT)
        kaskada.validate_client(client)
        req = table_pb.ListTablesRequest(**kwargs)
        return client.tableStub.ListTables(req, metadata=client.metadata)
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)

def get_table(**kwargs):
    """
    Gets a table by name
    """
    try:
        client = kwargs.pop('client', kaskada.KASKADA_DEFAULT_CLIENT)
        kaskada.validate_client(client)
        req = table_pb.GetTableRequest(**kwargs)
        return client.tableStub.GetTable(req, metadata=client.metadata)
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)

def create_table(**kwargs):
    """
    Creates a table
    """
    try:
        client = kwargs.pop('client', kaskada.KASKADA_DEFAULT_CLIENT)
        kaskada.validate_client(client)
        req = table_pb.CreateTableRequest(table = table_pb.Table(**kwargs))
        return client.tableStub.CreateTable(req, metadata=client.metadata)
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)

def delete_table(**kwargs):
    """
    Deletes a table
    """
    try:
        client = kwargs.pop('client', kaskada.KASKADA_DEFAULT_CLIENT)
        kaskada.validate_client(client)
        req = table_pb.DeleteTableRequest(**kwargs)
        return client.tableStub.DeleteTable(req, metadata=client.metadata)
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)

def load_data(table, staged_file, client: Client = None) -> table_pb.LoadDataResponse:
    """
    Loads data to a table from a staged file

    Args:
        table ([Table, CreateTableResponse, GetTableResponse, Str]): The target table object
        staged_file ([StagedFile, CreateStagedFileResponse, GetStagedFileResponse, Str]): The staged file object
        client (Client, optional): The Kaskada Client. Defaults to kaskada.KASKADA_DEFAULT_CLIENT.

    Raises:
        Exception: No valid table parameter provided
        Exception: No valid staged file ID parameter provided

    Returns:
        LoadDataResponse: Response from the API
    """
    if client == None:
        client = kaskada.KASKADA_DEFAULT_CLIENT

    table_name = None
    if isinstance(table, table_pb.Table):
        table_name = table.table_name
    elif isinstance(table, table_pb.CreateTableResponse) or isinstance(table, table_pb.GetTableResponse):
        table_name = table.table.table_name
    elif isinstance(table, str):
        table_name = table
    
    if table_name == None:
        raise Exception("invalid table parameter provided. the first parameter must be the table object, table response from the SDK, or the table name")
    
    staged_file_id = None
    if isinstance(staged_file, staged_pb.StagedFile):
        staged_file_id = staged_file.file_id
    elif isinstance(staged_file, staged_pb.CreateStagedFileResponse) or isinstance(staged_file, staged_pb.GetStagedFileResponse):
        staged_file_id = staged_file.file.file_id
    elif isinstance(staged_file, str):
        staged_file_id = staged_file
    
    if staged_file_id == None:
        raise Exception("invalid staged file parameter provided. the second parameter must be the staged file object, staged file response from the SDK, or the staged file ID")

    try:
        kaskada.validate_client(client)
        req = table_pb.LoadDataRequest(
            table_name = table_name,
            file_id = staged_file_id,
        )
        return client.tableStub.LoadData(req, metadata=client.metadata)
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)

def upload_file(table_name: str, file_path: str, client: Client = None):
    """
    Uploads a file directly to a table. Reads the file and uses the staging area to load the data.

    Args:
        table_name (str): The target table name
        file_path (str): The source local file path
        client (Client, optional): The Kaskada Client. Defaults to kaskada.KASKADA_DEFAULT_CLIENT.

    Returns:
        LoadDataResponse: Response from the API
    """
    if client == None:
        client = kaskada.KASKADA_DEFAULT_CLIENT
    f = open(file_path, 'rb')
    file_name = os.path.basename(f.name)
    staged_file = ks.create_staged_file(file_path, client = client)
    return load_data(table_name, staged_file)

def upload_dataframe(table_name: str, df: pd.DataFrame, client: Client = None):
    """
    Uploads a dataframe directly to a table. Writes the dataframe to a local file and loads the data to the table

    Args:
        table_name (str): The target table name
        df (pd.DataFrame): The source Pandas dataframe
        client (Client, optional): The Kaskada Client. Defaults to kaskada.KASKADA_DEFAULT_CLIENT.

    Returns:
        LoadDataResponse: Response from the API
    """
    if client == None:
        client = kaskada.KASKADA_DEFAULT_CLIENT
    staged_file = ks.create_staged_file(df, client = client)
    return load_data(table_name, staged_file)
