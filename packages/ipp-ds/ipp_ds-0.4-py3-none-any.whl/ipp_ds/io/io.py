import tempfile
from io import BytesIO, StringIO
from urllib.request import urlretrieve
from pptx import Presentation
from thinkcell import Thinkcell
import json

import pandas as pd
import numpy as np
import re

from azure.storage.blob import (BlobServiceClient)
from azure.identity import DefaultAzureCredential

import logging

# Set the logging level for all azure-* libraries
logger = logging.getLogger('azure')
logger.setLevel(logging.ERROR)

import warnings
warnings.filterwarnings('ignore')

DOWNLOAD_POOL_SIZE = 10

def create_blob_service(uri):

    credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)

    account_name = uri.replace('abfs://','').split('.')[0]

    blobService = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", 
                                    credential = credential)

    return blobService

def to_any(df, uri, _format, mode='pandas', encoding='utf-8', **kwargs):

    blob_service = create_blob_service(uri)
    container_name = uri.split('/')[3]
    blob_name = '/'.join(uri.split('/')[4:])

    blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)

    try:
        if _format not in ['csv', 'ppttc']:
            byte_stream = BytesIO()
        else:
            byte_stream = StringIO()

        if mode == 'pandas':
            format_map = {"parquet": df.to_parquet, "csv": df.to_csv, "excel": df.to_excel}
        if mode == 'pptx':
            format_map = {"pptx": df.save}
        if mode == 'thinkcell':
            format_map = {"ppttc": json.dump}

        func = format_map[_format]

        if _format not in ['csv', 'ppttc']:

            func(byte_stream, **kwargs)
            byte_stream.seek(0)
            blob_client.upload_blob(byte_stream, overwrite=True)

        else:
            if _format == 'ppttc':
                func(obj=df.charts, fp=byte_stream,**kwargs)

            else:
                func(byte_stream, encoding=encoding,**kwargs)

            byte_stream.seek(0)
            blob_client.upload_blob("".join(byte_stream.readlines()), overwrite=True)

    finally:
        byte_stream.close()



def read_any(uri, _format, mode='pandas',**kwargs):

    """ Get a dataframe from Parquet file on blob storage """
    blob_service = create_blob_service(uri)
    container_name = uri.split('/')[3]
    blob_name = '/'.join(uri.split('/')[4:])

    blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)

    try:

        byte_stream = BytesIO()
        byte_stream.write(blob_client.download_blob(max_concurrency=16).readall())
        byte_stream.seek(0)

        if mode == 'pandas':
            format_map = {"parquet": pd.read_parquet, "csv": pd.read_csv, "xls": pd.read_excel}
        if mode == 'pptx':
            format_map = {'pptx': Presentation}

        if mode == 'thinkcell':
            df = Thinkcell()
            df.add_template(uri)

        if mode != 'thinkcell':
            func = format_map[_format]
            df = func(byte_stream, **kwargs)

    finally:
        byte_stream.close()

    return df


def to_parquet(df: pd.DataFrame, uri, **kwargs):
    return to_any(df, uri, "parquet", **kwargs)


def to_excel(df: pd.DataFrame, uri, **kwargs):
    return to_any(df, uri, "excel", **kwargs)

def to_ppttc(df, uri, **kwargs):
    return to_any(df, uri, "ppttc", mode='thinkcell', **kwargs)

def to_csv(df: pd.DataFrame, uri, encoding='utf-8', **kwargs):
    return to_any(df, uri, "csv", encoding=encoding,**kwargs)

def to_pptx(df, uri, **kwargs):
    return to_any(df, uri, "pptx", mode='pptx', **kwargs)

def walk(uri, **kwargs):

    blob_service = create_blob_service(uri)
    container_name = uri.split('/')[3]
    blob_name = '/'.join(uri.split('/')[4:])
    url_name = '/'.join(uri.split('/')[:4])
    container_client = blob_service.get_container_client(container=container_name)
    list_blobs = [url_name+'/'+unit['name'] for unit in container_client.list_blobs(name_starts_with=f'{blob_name}/')]

    return list_blobs


def glob(uri, **kwargs):

    path_suffix = uri.split("*")[1]
    uri = uri.split("*")[0]
    blob_service = create_blob_service(uri)
    container_name = uri.split('/')[3]
    blob_name = '/'.join(uri.split('/')[4:])
    url_name = '/'.join(uri.split('/')[:3])
    container_client = blob_service.get_container_client(container=container_name)
    list_blobs = [url_name+'/'+container_name+'/'+unit['name'] for unit in container_client.list_blobs(name_starts_with=f'{blob_name}')]

    result_list = []
    for i in np.array(list_blobs):
        try:
            match = re.search(r".+" + path_suffix + r".*", i)
            result_list.append(str(match.group()))
        except:
            next

    return result_list

def read_parquet(uri, mode='pandas', **kwargs):
    return read_any(uri, "parquet", mode=mode, **kwargs)


def read_csv(uri, mode='pandas', **kwargs):
    return read_any(uri, "csv", mode=mode, **kwargs)


def read_excel(uri, mode='pandas', **kwargs):
    return read_any(uri, "xls", mode=mode, **kwargs)

def read_pptx(uri, mode='pptx', **kwargs):
    return read_any(uri, "pptx", mode=mode, **kwargs)

def read_tc_template(uri, _format='pptx', mode='thinkcell', **kwargs):
    return read_any(uri, "pptx", mode=mode, **kwargs)

def read_url(uri, sas_token, _format, **kwargs):
    """Read from a container with SAS token """
    with tempfile.NamedTemporaryFile() as tf:
        url_tok = uri + sas_token
        urlretrieve(url_tok, tf.name)
        df = read_any(uri=tf.name, _format=_format, **kwargs)
        return df


def file_exists(path):
    """ Checa se o arquivo informado existe """
    last_dir = path.replace(path.split('/')[-1], "*")

    if path in glob(last_dir):
        return True
    else:
        return False
