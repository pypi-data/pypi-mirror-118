#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import logging
import random
import time
import types
from functools import wraps
from traceback import format_exc

from bson.objectid import ObjectId
from tornado.web import HTTPError
from tornado.web import RequestHandler
from lcyframe.libs import errors
from lcyframe.libs import utils
from lcyframe.libs.funts import get_params, get_return
from lcyframe.libs.permissions import Permission


class BaseHandler(RequestHandler):
    __structure__ = {}

    def __init__(self, application, request, **kwargs):
        self.application = application
        self.request = request
        super(BaseHandler, self).__init__(application, request, **kwargs)
        if request.headers.get("cdn-src-ip", None):
            request.remote_ip = request.headers["cdn-src-ip"]
        elif request.headers.get("X-Forwarded-For", None):
            try:
                request.remote_ip = request.headers["X-Forwarded-For"].split(",")[0]
            except Exception as e:
                request.remote_ip = self.request.headers.get('X-Real-Ip', '')
        self.cors_config = self.application.app_config.get("cors_config", {})

    def prepare(self):
        if self.request.method == "OPTIONS" and self._allow_cors:
            self.set_cors_header()
            self.set_status(204)
            self.finish()
            return

    @property
    def _allow_cors(self):
        """
        校验授信跨域来路
        :return:
        """
        self.cors_config = self.application.app_config.get("cors_config", {})
        allow = self.cors_config and self.cors_config.get("allow", False)
        self.origin = self.request.headers.get("origin")
        self.cors_config["origin"].append(self.application.app_config["wsgi"]["host"])
        auto_origin = self.cors_config["origin"]
        if not allow or ("*" not in auto_origin and self.origin not in auto_origin):
            raise errors.ErrorCorsUri
        return True

    def set_cors_header(self):
        """通过授信校验后，允许设置响应头"""
        self.set_header("Content-Type", self.cors_config.get("content-type", "text/html") + "; charset=utf-8")
        self.set_header("Access-Control-Allow-Origin", "*" if "*" in self.cors_config.get("origin", "origin") else self.request.headers.get("origin", ""))
        self.set_header("Access-Control-Allow-Headers", ",".join(self.cors_config.get("headers", ["*"])))
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Methods", ",".join(self.cors_config.get("methods", ["GET", "POST", "PUT", "DELETE"])))
        self.set_header("Access-Control-Max-Age", self.cors_config.get("max-age", 60))

    def write_error(self, status_code, **kwargs):
        self.cors_config = self.application.app_config.get("cors_config", {})
        allow = self.cors_config and self.cors_config.get("allow", False)
        if allow:
            self.set_cors_header()

        if status_code == 404:
            return self.write_failed(code=status_code, msg="Not found", name="HTTP 404")
        elif status_code == 405:
            logging.warning("HTTP 405: Method/URL Not Allowed")
            return self.write_failed(code=status_code, msg="HTTP 405: Method/URL Not Allowed", name="HTTP 405")
        elif status_code == 500:
            error = kwargs["exc_info"][1]
            logging.warning("时间：" + self.utils.int_to_date_string(self.utils.now(), "%Y-%m-%d %H:%M:%S"))
            if not hasattr(error, "message"):
                message = error.args[0] if error.args else "未知错误"
            else:
                message = error.message

            logging.warning(message)
            if not hasattr(error, "code_name") or not hasattr(error, "code"):
                return self.write_failed()
            else:
                return self.write_failed(code=error.code, msg=error.message, name=error.code_name)
        else:
            return self.write_failed()

    def write_success(self, data=None):
        request_time = 1000.0 * self.request.request_time()
        if self.application.app_config.get("logging_config", {}).get("level", "debug") != "debug":
            if request_time > int(self.application.app_config["wsgi"].get("slow_request_time", 1000)):
                logging.warning("%d %s %.2fms", self.get_status(),
                                self._request_summary(), request_time)
        if hasattr(self, "graylog"):
            p = self.params if hasattr(self, "params") else {}
            self.graylog.from_server(short_message="OK", code=0, host=self.request.host, request_time=int(request_time), remote_ip=self.request.remote_ip,
                                     uri=self.request.path, params=p, method=self.request.method)
        return self.write({"code": 0, "msg": "OK", "data": get_return(self, data or {})})

    def write_failed(self, code=1, msg="Error. unknown error", name="HTTP 500"):
        if hasattr(self, "graylog"):
            p = self.params if hasattr(self, "params") else {}
            self.graylog.from_server(short_message=msg, code=code, track=format_exc()[-10:], host=self.request.host, header=self.request.headers._dict,
                                     remote_ip=self.request.remote_ip, uri=self.request.path, params=p, method=self.request.method)
        if name:
            self.write({"code": code, "msg": msg, "name": name, "data": None})
            return
        else:
            self.write({"code": code, "msg": msg, "data": None})
            return

    def write(self, chunk):
        chunk = json.dumps(chunk, ensure_ascii=False)
        return super(BaseHandler, self).write(chunk)

    def json_callback(self, data):
        """json回调跨域
        """
        jsoncallback = self.get_argument("jsoncallback", None)
        if jsoncallback:
            self.write("%s(%s)" % (jsoncallback, json.dumps(data)))
        else:
            self.write(data)

    def restrict(self, count, duration=60):
        """接口访问限制"""

        def wrap(method):
            @wraps(method)
            def has_role(self, *args, **kwargs):
                if not hasattr(self, "redis"):
                    return method(self, *args, **kwargs)

                # 获取客户端ip
                ip = None
                if self.request.headers.get("cdn-src-ip"):
                    ip = self.request.headers.get("cdn-src-ip")
                elif self.request.headers.get("X-Forwarded-For"):
                    z = self.request.headers["X-Forwarded-For"].split(",")
                    if len(z) > 0:
                        ip = z[0]
                ip = ip or self.request.remote_ip

                n = self.redis.incr("restrict:%s" % ip)

                if n == 1:
                    self.redis.expire("restrict:%s" % ip, duration)
                elif n > count:
                    raise HTTPError(503, "Slow Down")

                return method(self, *args, **kwargs)

            return has_role

        return wrap

    @property
    def utils(self):
        return utils

    @property
    def api_error(self):
        return errors

    def get_headers(self, HEADERS=dict()):
        _headers = {}
        if not HEADERS:
            for k, v in self.request.headers.items():
                _headers[k.lower()] = v

        for k, v in HEADERS.items():
            value = self.request.headers.get(k)
            if value is None:
                # 客户端没有传值, 按照默认值类型赋值
                value = v(value) if isinstance(v, types.FunctionType) else v
            else:
                # 按照默认值的类型 转换参数
                value = utils.TypeConvert.apply(v, value)

            _headers[k] = value

        return _headers

    @property
    def Permission(self):
        return Permission.initial()

    @property
    def app_config(self):
        return self.application.app_config

    @property
    def model(self):
        return BaseModel.model



class BaseModel(object):
    utils = utils
    Permission = None
    mongo = None
    mysql = None
    redis = None
    ssdb = None
    mq = None
    nsq = None
    celery = None
    api_error = None
    app_config = {}
    model = None

    @classmethod
    def _parse_data(cls, d, **kwargs):
        """
        组装单条数据
        :return:
        :rtype:
        """
        return_data = {}
        if not d:
            return {}

        for k, v in d.items():
            # if k in ["pass_word", "salt", "permission"] and k not in kwargs.get("kwargs", {}):
            #     continue
            return_data[k] = v

        return return_data


class BaseSchema(object):
    """
    is_shard = True                           # 是否分表
    shard_key = "uid"                         # 分表键
    shard_rule()                              # 分表规则，允许复写
    """
    collection = ""
    is_shard = False
    shard_key = ""

    @classmethod
    def fields(cls):
        return vars(cls())

    @classmethod
    def shard_rule(cls, shard_key_value):
        """
        :param shard_key_value:
        :return: table_value

        This is default rule by `mod10`
        you can overwriter like this

        :example ::
            def shard_rule(shard_key_value):
                do_your_thing
                ...
        """
        return cls.mod10(shard_key_value)

    @classmethod
    def get_shard_table(cls, sql=None, shard_key_value=None):
        """
        默认分表规则
        可以在从schema中复写该方法
        :param shard_key:
        :return:
        """
        if cls.is_shard:
            assert sql is not None or shard_key_value is not None
            assert cls.shard_key in cls.fields()
            value = shard_key_value if shard_key_value is not None else cls.get_value_with_sql(sql)
            return cls.collection + "_" + str(cls.shard_rule(value))
        else:
            return cls.collection

    @classmethod
    def get_value_with_sql(cls, sql):
        """
        :param sql:
        :return:
        """
        if cls.shard_key not in sql:
            raise KeyError("When shard table, shard key must in sql")
        return sql[cls.shard_key]

    @classmethod
    def mod10(cls, shard_key_value=None):
        """
        取模10
        :param mod:
        :return:
        """
        if type(shard_key_value) != int:
            raise KeyError("When shard table, shard key type must int")
        return shard_key_value % 10

    @classmethod
    def dbo(cls, sql=None, shard_key_value=None):
        return cls.mongo[cls.get_shard_table(sql=sql, shard_key_value=shard_key_value)]

    @classmethod
    def insert(cls, docs, shard_key_value=None):
        doc_or_docs = []
        if not docs:
            return None

        if not isinstance(docs, list):
            insert_docs = [docs]
        else:
            insert_docs = docs

        for d in insert_docs:
            d["create_at"] = utils.now()
            s = vars(cls())
            s.update(d)
            doc_or_docs.append(s)

        data = cls.dbo(sql=docs, shard_key_value=shard_key_value).insert(doc_or_docs)

        data = list(map(str, data))

        return str(data[0]) if not isinstance(docs, list) else map(str, data)

    @classmethod
    def remove(cls, spec, shard_key_value=None):
        spec = cls.__check_id(spec)
        return cls.dbo(sql=spec, shard_key_value=shard_key_value).remove(spec)

    @classmethod
    def find_one_by_oid(cls, oid, shard_key_value=None):
        """

        :param oid: ObjectId
        :return:
        """
        return cls.find_one({"_id": oid}, shard_key_value=shard_key_value)

    @classmethod
    def find_one(cls, spec=None, shard_key_value=None):
        spec = cls.__check_id(spec)
        d = cls.dbo(sql=spec, shard_key_value=shard_key_value).find_one(spec or {}) or {}
        return cls.__parse_oid(d)

    @classmethod
    def find(cls, spec=None, fields=False, limit=False, skip=False, sort=False, is_cursor=False, shard_key_value=None):
        """

        :param spec:
        :param cursor:  True 返回游标，否则返回list
        :return:
        """
        spec = cls.__check_id(spec)
        data = []
        spec = spec or {}
        if type(sort) == dict:
            sort = sort.items()
        if fields and isinstance(fields, dict):
            cursor = cls.dbo(sql=spec, shard_key_value=shard_key_value).find(spec, fields)
        else:
            cursor = cls.dbo(sql=spec, shard_key_value=shard_key_value).find(spec)

        if limit is not False:
            cursor = cursor.limit(int(limit))
        if skip is not False:
            cursor = cursor.skip(int(skip))
        if sort is not False:
            cursor = cursor.sort(sort)

        if is_cursor:
            return cursor

        for d in cursor:
            data.append(cls.__parse_oid(d))

        return data

    @classmethod
    def distinct(cls, spec, distinct, shard_key_value=None):
        """
        按distinct 过滤重复
        :param spec:
        :param distinct:
        :return:
        """
        spec = cls.__check_id(spec)
        return cls.find(spec, is_cursor=True, shard_key_value=shard_key_value).distinct(distinct)

    @classmethod
    def aggregate(cls, pipeline, shard_key_value=None):
        return cls.dbo(shard_key_value=shard_key_value).aggregate(pipeline)

    @classmethod
    def update(cls, spec=None, docs=None, check_updated_state=True, shard_key_value=None, **kwargs):
        """
        wrap collection's update
        :param spec: 更新条件
        :param docs: 更新文档
        :param check_updated_state: True 直接返回是否成功更新状态字段值(updatedExisting)
        False 返回完整的更新结果
        :param kwargs:
        """
        if docs is None:
            raise Exception('document is None!')
        if spec is None:
            raise Exception('spec is None!')

        spec = cls.__check_id(spec)

        if not any(k.startswith('$') for k in docs.keys()):
            docs = {"$set": docs}

        docs.setdefault("$set", {})['update_at'] = utils.now()

        result = cls.dbo(sql=spec, shard_key_value=shard_key_value).update(spec, docs, **kwargs)
        return result.get('updatedExisting') if check_updated_state else result

    @classmethod
    def find_and_modify(cls, spec, docs, shard_key_value=None, **kwargs):
        spec = cls.__check_id(spec)
        docs.setdefault("$set", {})['update_at'] = utils.now()

        kwargs["new"] = kwargs.get("new", True)
        d = cls.dbo(sql=spec, shard_key_value=shard_key_value).find_and_modify(spec,
                                                                               docs,
                                                                               upsert=kwargs.pop("upsert", True),
                                                                               sort=kwargs.pop("sort", None),
                                                                               full_response=kwargs.pop("full_response", False),
                                                                               manipulate=kwargs.pop("manipulate", False), **kwargs)
        return cls.__parse_oid(d)

    @classmethod
    def find_list_by_page(cls, spec, page, count=10, sort={"create_at": -1}, fields=False, shard_key_value=None):
        """
        按照count分页，返回当前页数据和总页数
        :param spec:
        :param count:
        :param sort: must be obj like [("a", -1), ...]
        :return:
        """
        cursor = cls.find(spec, fields=fields, is_cursor=True, shard_key_value=shard_key_value)
        data_list = [cls.__parse_oid(c) for c in list(cls.__meta_cursor(cursor, page, count, sort))]
        total_page = cls.__get_total_page(cursor, count)
        return data_list, total_page

    @classmethod
    def find_list_by_last_id(cls, spec, count=10, sort={"create_at": -1}, fields=False, last_id_field=False, shard_key_value=None):
        """
        list by last_id
        :param spec:
        :param count:
        :param sort: must be obj like [("a", -1), ...]
        :return:
        """
        cursor = cls.find(spec, fields=fields, is_cursor=True, shard_key_value=shard_key_value)
        data_list = [cls.__parse_oid(c) for c in list(cls.__meta_cursor(cursor, count=count, sort=sort))]
        last_id_field = last_id_field if last_id_field else "create_at"
        last_id = data_list[-1][last_id_field] - 1 if data_list else -1
        return data_list, last_id

    @classmethod
    def get_batch_data(cls, *vals, **kwargs):
        """
        批量获取一批数据
        :param k:
        :param vals:
        :return:
        """
        key = kwargs.pop("key", "_id")
        data_mp = {}
        skip_field_list = kwargs.get("skip_field_list", [])

        data, __ = cls.find_list_by_page({key: {"$in": vals}}, 0, 0, **kwargs)
        for d in data:
            d = cls.__parse_oid(d)
            tmp = {}
            for k, v in d.items():
                if k in skip_field_list:
                    continue
                tmp[k] = v

            data_mp[d[key]] = tmp

        return data_mp

    @classmethod
    def next_seq_id(cls, seq_name="seq_id", val=0, random_step=10):
        """Generate next value
        :param val: step value
        :return: :rtype:
        """
        if not val:
            val = random.randrange(1, random_step)

        result = cls.mongo.sequence.find_and_modify({'seq_name': seq_name}, {'$inc': {'val': val}}, True, new=True)

        if result:
            return result['val']
        return None

    @classmethod
    def __meta_cursor(cls, cursor, page=None, count=10, sort=dict()):
        sort = sort.items() if type(sort) == dict else list(sort) if sort else False

        if page:
            skip = (int(page) - 1) * int(count)
            cursor.skip(skip)

        if count:
            cursor = cursor.limit(int(count))

        if sort:
            cursor = cursor.sort(sort)

        return cursor

    @classmethod
    def __get_total_page(cls, cursor, count=10):
        if not count:
            return 1
        c = cursor.count() / count
        s = cursor.count() % count
        return c + 1 if s else c

    @classmethod
    def __parse_oid(cls, d):
        if not d:
            d = {}
        if d and isinstance(d.get("_id"), ObjectId):
            d["_id"] = str(d["_id"])
        return d

    @classmethod
    def __check_id(cls, spec):
        if not spec:
            return spec

        for k, v in spec.items():
            if k == "_id":
                if isinstance(v, dict):
                    if v.keys()[0] in ["$in", "$nin"]:
                        sin = v.keys()[0]
                        v[sin] = list(map(utils.to_ObjectId, spec[k][sin]))
                    else:
                        continue

                    spec[k] = v
                elif isinstance(v, list):
                    spec[k] = list(map(utils.to_ObjectId, spec[k]))
                else:
                    spec[k] = utils.to_ObjectId(v)
        return spec
