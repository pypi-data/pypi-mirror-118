# coding=utf-8
import datetime
import logging
import redis
import pyssdb
import nsq
import threading
from lcyframe.libs.emchat import EMChatAsync
from lcyframe.libs.hot_queue import HotQueue
from lcyframe.libs.mob_sms import MobSMS
from lcyframe.libs.mqtt_route import ConnectMqtt
try:
    from AsyncQiniu.sevencow import Cow as Qiniu
except:
    pass

try:
    from pymongo import MongoClient, ReadPreference
except:
    print("not found model pymongo")

# try:
#     from database.base_mysqldb import MysqlDb
# except:
#     print("not found model MysqlDB")
#

class MongoCon(object):
    """mongodb数据库连接单例类"""
    _database = {}

    @classmethod
    def get_connection(cls, **kwargs):
        """返回全局的数据库连接
        return mongodb connection
        """
        options = {}
        hosts = [kwargs.get("host", "localhost") + ":" + str(kwargs.get("port", "27017"))]

        # 或者
        # options["host"] = kwargs.get("host", "localhost")
        # options["port"] = kwargs.get("port", "27017")
        is_repliset = kwargs.get("model", "").lower() in ["repliset", "replica"]

        if is_repliset:
            for slave in kwargs.get("slaves", []):
                hosts.append(slave["host"] + ":" + str(slave["port"]))

            options["replicaSet"] = kwargs["replsetName"]
            read_preference = kwargs.get("read_preference", "primary")
            mp = {
                "primary": ReadPreference.PRIMARY,
                "primaryPreferred": ReadPreference.PRIMARY_PREFERRED,
                "secondary": ReadPreference.SECONDARY,
                "secondaryPreferred": ReadPreference.SECONDARY_PREFERRED,
                "nearest": ReadPreference.PRIMARY,

            }
            options["read_preference"] = mp[read_preference]

        options["host"] = hosts

        if kwargs.get("username"):
            options["username"] = kwargs["username"]
            options["password"] = kwargs["password"]

        return MongoClient(**options)

    @classmethod
    def get_database(cls, **kwargs):
        """返回当前数据库
        return mongodb database
        """
        hosts = kwargs.get("host", "localhost") + ":" + str(kwargs.get("port", "27017"))
        conn_key = "%s.%s" % (hosts, kwargs.get("database", "test"))
        if conn_key not in cls._database:
            cls._database[conn_key] = cls.get_connection(**kwargs)[kwargs.get("database", "test")]
        return cls._database[conn_key]


class PyMysqlCon(object):
    _mysql = None

    @classmethod
    def get_connection(cls, **kwargs):
        mode = int(kwargs.get("mode", 3))    # 连接模式 1 PyMysqlCon，2 PyMysqlThreadCon， 3 PyMysqlPooledDB， 4 PyMysqlPersistentDB
        from lcyframe.libs.database.base_pymysql import PyMysqlPooledDB, PyMysqlPersistentDB
        mp = {
            # 1: PyMysqlCon,
            # 2: PyMysqlThreadCon,
            3: PyMysqlPooledDB,
            4: PyMysqlPersistentDB
        }
        if cls._mysql is None:
            cls._mysql = mp[mode](**kwargs)
        return cls._mysql


class RedisCon(object):
    """redis连接单例类"""
    _redis = None

    @classmethod
    def get_connection(cls, **kwargs):
        if cls._redis is None:
            cls._redis = redis.Redis(**kwargs)
        return cls._redis


class SSDBCon(object):
    """SSDB连接单例类"""
    _ssdb = None

    @classmethod
    def get_connection(cls, **kwargs):
        if cls._ssdb is None:
            cls._ssdb = pyssdb.Client(kwargs.get("host", "127.0.0.1"), int(kwargs.get("port", 8888)), max_connections=1048576)
        return cls._ssdb


class MQCon(object):
    """message queue 连接单例类"""
    _mq = None

    @classmethod
    def get_connection(cls, **kwargs):
        if cls._mq is None:
            import json
            cls._mq = HotQueue(name=kwargs.get("name", "mq"),
                               serializer=json,     # pickle has a decode error with py3
                               host=kwargs.get("host", "127.0.0.1"),
                               port=int(kwargs.get("port", 6379)),
                               db=kwargs.get("db", 0))
        return cls._mq


class NsqCon(object):
    """message nsq 连接单例类"""
    _nsq = None

    @classmethod
    def get_connection(cls, **kwargs):
        if cls._nsq is None:
            cls._nsq = nsq.Writer(kwargs.get("nsqd_tcp_addresses", "127.0.0.1:4150"))
        return cls._nsq


class MqttCon(object):
    """message mqtt 连接单例类"""
    _mqtt = None

    @classmethod
    def get_connection(cls, **kwargs):
        if cls._mqtt is None:
            # 代理模式，使用publish.single()提交数据
            # from mqtt_route import ReadMqtt
            # cls._mqtt = ReadMqtt(**kwargs)

            # 生产者长连接, loop_start()用一个独立线程保持连接，代替每次loop()；消费客户端使用loop_forever()轮训；二者互斥，单线程内互踢链接。
            cls._mqtt = ConnectMqtt(**kwargs).mqttc
        return cls._mqtt


class EmchatCon(object):
    """message queue 连接单例类"""
    _emchat = None

    @classmethod
    def get_connection(cls, **kwargs):
        if cls._emchat is None:
            cls._emchat = EMChatAsync(**kwargs)
        return cls._emchat


class MobCon(object):
    """message queue 连接单例类"""
    _mob = None

    @classmethod
    def get_connection(cls, **kwargs):
        if cls._mob is None:
            cls._mob = MobSMS(**kwargs)
        return cls._mob


class QinNiuCon(object):
    """message queue 连接单例类"""
    _qiniu = None

    @classmethod
    def get_connection(cls, **kwargs):
        if cls._qiniu is None:
            cls._qiniu = Qiniu(**kwargs)
        return cls._qiniu


class CeleryCon(object):
    _app = None
    _instance_lock = threading.Lock()

    @classmethod
    def get_connection(cls, **kwargs):
        if cls._app is None:
            from .celery_route import MyCelery
            cls._app = MyCelery(kwargs.get("project", "lcyframe-celery"))
            # app.config_from_object("celeryconfig")
            # os.environ['CELERY_CONFIG_MODULE'] = 'celeryconfig'
            cls._app.config_from_envvar('CELERY_CONFIG_MODULE')
        return cls._app



    # @classmethod
    # def get_connection(cls, **kwargs):
    #     if not hasattr(CeleryCon, "_app"):
    #         with CeleryCon._instance_lock:
    #             if not hasattr(CeleryCon, "_app"):
    #                 from celery_route import MyCelery
    #                 CeleryCon._app = MyCelery(kwargs.get("project", "lcyframe-celery"))
    #                 # app.config_from_object("celeryconfig")
    #                 # os.environ['CELERY_CONFIG_MODULE'] = 'celeryconfig'
    #                 CeleryCon._app.config_from_envvar('CELERY_CONFIG_MODULE')
    #     return CeleryCon._app

class BeanstalkCon(object):
    _conn = None

    @classmethod
    def get_connection(cls, **kwargs):
        if cls._conn is None:
            from .beanstalk import BeanStalk
            cls._conn = BeanStalk(host=kwargs["host"], port=kwargs["port"], use=kwargs.get("use", "default"), watch=kwargs.get("use", "default"))

        return cls._conn

class GrayLogCon(object):
    """
    收集异常日志、定向发送日志
    """
    _instance_lock = threading.Lock()

    def __init__(self, **kwargs):
        from gelfclient import UdpClient
        try:
            self.graylog = UdpClient(kwargs.get("host", '127.0.0.1'), kwargs.get("port", 12201))
        except Exception as e:
            self.graylog = GrayLogCon()

    def __new__(cls, **kwargs):
        if not hasattr(GrayLogCon, "_instance"):
            with GrayLogCon._instance_lock:
                if not hasattr(GrayLogCon, "_instance"):
                    GrayLogCon._instance = object.__new__(cls)
        return GrayLogCon._instance

    def send(self, **data):
        """
        发送日志
        :param data:
        :return:
        """
        try:
            default = {
                "level": 1,
                "track": "",
                "host": "",
                # "timestamp": "2021-05-10 18:47:21.576 +08:00",
                "short_message": "null"
            }
            default.update(data)
            if self.graylog is None:
                logging.warning("Graylog Connection Loss.")
            else:
                self.graylog.log(default)
        except Exception as e:
            logging.warning(e)

    def from_server(self, **data):
        data["app"] = "server"
        return self.send(**data)

    def from_mongo(self, **data):
        data["app"] = "mongo"
        return self.send(**data)

    def from_mysql(self, **data):
        data["app"] = "mysql"
        return self.send(**data)

    def from_mq(self, **data):
        data["app"] = "mq"
        return self.send(**data)

