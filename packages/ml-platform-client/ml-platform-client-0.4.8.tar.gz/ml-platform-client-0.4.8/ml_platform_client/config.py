import os

from ml_platform_client.constants import MODE_CLUSTER


class ClientConfig:
    def __init__(self):
        self.minio_host = os.environ.get("MINIO_HOST", "172.17.0.1:9000")
        self.minio_access_key = os.environ.get(
            "MINIO_ACCESS_KEY", "24WTCKX23M0MRI6BA72Y"
        )
        self.minio_secret_key = os.environ.get(
            "MINIO_SECRET_KEY", "6mxoQMf1Lha2q1H3fp3fjNHEZRJJ7LvbC5k3+CQX"
        )
        self.minio_secure = os.environ.get("MINIO_SECURE", "false") in ["true", "True"]
        self.db_host = os.environ.get("DB_HOST", "172.17.0.1")
        self.db_port = int(os.environ.get("DB_PORT", 3306))
        self.db_user = os.environ.get("DB_USER", "root")
        self.db_password = os.environ.get("DB_PASS", "password")
        self.db_type = os.environ.get("MLP_CLIENT_DB_TYPE", "mysql")
        self.db_schema = os.environ.get("MLP_CLIENT_DB_SCHEMA", 'ml_platform')
        self.db_name = os.environ.get("ML_CLIENT_MLP_DB_NAME", "ml_platform")

        self.kafka_host = os.environ.get("KAFKA_SERVERS", "172.17.0.1:9092")
        self.kafka_username = os.environ.get("KAFKA_USERNAME", "emotibot")
        self.kafka_password = os.environ.get("KAFKA_PASSWORD", "xOPJk9py4K1S")
        self.num_worker = int(os.environ.get("MLP_CLIENT_WORKER", 5))
        self.num_thread = int(os.environ.get("MLP_CLIENT_THREAD", 10))
        self.mode = os.environ.get("MLP_CLIENT_MODE", MODE_CLUSTER)
        self.checker_start = os.environ.get('CHECKER_START', 'true') in ['true', 'True']
        self.connect_kafka = os.environ.get('CONNECT_KAFKA', 'true') in ['true', 'True']


client_config = ClientConfig()
