import os
import traceback

import time
from minio import Minio

from .config import client_config
from .logger import log
if client_config.connect_kafka:
    from .kafka_accessor import train_tracker


class MinIOAccessor:
    _client = None
    max_retry = 3

    @staticmethod
    def init_client(host, access_key, secret_key, secure):
        minio_client_instance = Minio(
            host, access_key=access_key, secret_key=secret_key, secure=secure
        )
        log.info(
            "minio connection info: host={}, access_key={}, secret_key={}, secure={}".format(
                host, access_key, secret_key, secure
            )
        )
        MinIOAccessor._client = minio_client_instance

    @staticmethod
    def get_client(remote_host=None) -> Minio:
        if MinIOAccessor._client is None:
            if remote_host:
                host = remote_host
            else:
                host = client_config.minio_host
            MinIOAccessor.init_client(
                host,
                client_config.minio_access_key,
                client_config.minio_secret_key,
                client_config.minio_secure,
            )
            # raise Exception('client is not initialized')
        return MinIOAccessor._client

    @staticmethod
    def fget_object(filepath: str, save_path: str, remote_host=None):
        pos = filepath.index("/")
        bucket = filepath[:pos]
        filepath = filepath[pos + 1 :]
        retry = 0
        while retry < MinIOAccessor.max_retry:
            try:
                MinIOAccessor.get_client(remote_host).fget_object(
                    bucket, filepath, save_path
                )
                log.info(
                    "read file from minio success: {}.{}".format(
                        bucket, filepath, retry
                    )
                )
                return
            except Exception as e:
                log.error(
                    "read file from minio error: {}.{}, retry:{}".format(
                        bucket, filepath, retry
                    )
                )
                log.error(e)
                traceback.print_exc()
                retry += 1
                time.sleep(2)
        log.error("read file from minio fail: {}.{}".format(bucket, filepath))
        if client_config.connect_kafka:
            train_tracker.send(message="read file from minio error", reason=e)
        raise Exception("read file from minio error exceed max retry")

    @staticmethod
    def save_object(local_path: str, remote_path: str, remote_host=None):
        pos = remote_path.index("/")
        bucket = remote_path[:pos]
        filepath = remote_path[pos + 1 :]
        with open(local_path, "rb") as file_data:
            file_stat = os.stat(local_path)
            try:
                MinIOAccessor.get_client(remote_host).put_object(
                    bucket, filepath, file_data, file_stat.st_size
                )
            except Exception as e:
                if client_config.connect_kafka:
                    train_tracker.send(message="upload file to minio error", reason=e)

    @staticmethod
    def delete(bucket, prefix: str, recursive=False, remote_host=None):
        objs = MinIOAccessor.get_client(remote_host).list_objects(
            bucket, prefix, recursive
        )
        for obj in objs:
            try:
                MinIOAccessor.get_client(remote_host).remove_object(
                    bucket, obj.object_name
                )
            except Exception as e:
                if client_config.connect_kafka:
                    train_tracker.send(message="delete minio file error", reason=e)
