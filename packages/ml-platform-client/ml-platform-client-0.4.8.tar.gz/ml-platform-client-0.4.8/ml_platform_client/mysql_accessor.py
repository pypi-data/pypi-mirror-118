from re import S
import sqlalchemy as sa
from urllib.parse import quote_plus
from .constants import TRAIN_STATUS_TRAINING, TRAIN_STATUS_UNKNOWN
from .constants import TRAIN_STATUS_ERROR, TRAIN_STATUS_COMPLETED
from .config import client_config


class SqlHelper:
    engine = None
    meta = None
    t_model = None
    t_load_record = None

    def __init__(self):

        # build common addr
        mysql_host = client_config.db_host
        mysql_port = client_config.db_port
        mysql_user = client_config.db_user
        mysql_password = client_config.db_password
        addr = f'{mysql_user}:{quote_plus(mysql_password)}@{mysql_host}:{mysql_port}'

        # build real addr and table args
        db_type = str(client_config.db_type).lower()
        if db_type in ('mssql', 'sqlserver'):
            addr = f'mssql+pymssql://{addr}/{client_config.db_name}?charset=utf8'
            table_args = {'schema': client_config.db_schema}
        elif db_type in ('pg', 'postgres', 'postgresql'):
            addr = f'postgresql+psycopg2://{addr}/{client_config.db_name}'
            table_args = {}
        else:
            addr = f'mysql+pymysql://{addr}/{client_config.db_name}'
            table_args = {}
        # create engine
        self.engine = sa.create_engine(
            addr,
            pool_pre_ping=True
        )
        # define tables
        self.meta = sa.MetaData()
        self.t_model = sa.Table(
            'model',
            self.meta,
            sa.Column('model_id'),
            sa.Column('path'),
            sa.Column('status'),
            sa.Column('loaded'),
            sa.Column('algorithm'),
            **table_args,
        )
        self.t_load_record = sa.Table(
            'load_record', 
            self.meta,
            sa.Column('load_time'),
            sa.Column('algorithm'),
            **table_args,
        )


class MysqlAccessor:
    _sql_helper = None
    _engine = None
    _t_model = None
    _t_load_record = None

    @staticmethod
    def get_sql_helper():
        if MysqlAccessor._sql_helper is None:
            MysqlAccessor._sql_helper = SqlHelper()
        return MysqlAccessor._sql_helper

    @staticmethod
    def get_engine():
        return MysqlAccessor.get_sql_helper().engine

    @staticmethod
    def check_load_update_time(algorithm):
        t = MysqlAccessor.get_sql_helper().t_load_record
        with MysqlAccessor.get_engine().connect() as conn:
            stmt = sa.select([
                t.c.load_time
            ]).where(t.c.algorithm == algorithm)
            return conn.execute(stmt).scalar()

    @staticmethod
    def get_load_models(algorithm):
        t = MysqlAccessor.get_sql_helper().t_model
        with MysqlAccessor.get_engine().connect() as conn:
            stmt = sa.select([
                t.c.model_id,
                t.c.path,
            ]).where(
                (t.c.algorithm == algorithm)
                & (t.c.loaded == 1)
            )
            res = conn.execute(stmt).fetchall()
            return {model_id: model_path for model_id, model_path in res}

    @staticmethod
    def get_model_train_status(model_id):
        t = MysqlAccessor.get_sql_helper().t_model
        with MysqlAccessor.get_engine().connect() as conn:
            stmt = sa.select([
                t.c.status,
            ]).where(
                (t.c.model_id == model_id)
            )
            status = conn.execute(stmt).scalar()
            if not status:
                return TRAIN_STATUS_UNKNOWN
            if status == 'active' or status == 'inactive':
                return TRAIN_STATUS_COMPLETED
            if status == 'error':
                return TRAIN_STATUS_ERROR
            return TRAIN_STATUS_TRAINING

    @staticmethod
    def update_model_train_status(model_id, status):
        t = MysqlAccessor.get_sql_helper().t_model
        with MysqlAccessor.get_engine().begin() as conn:
            stmt = t.update().values(
                status=status,
            ).where(
                (t.c.model_id == model_id)
                & (t.c.status == 'training')
            )
            conn.execute(stmt)
        return

