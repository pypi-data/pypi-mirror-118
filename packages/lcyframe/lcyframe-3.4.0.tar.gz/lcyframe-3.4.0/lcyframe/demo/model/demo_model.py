#!/usr/bin/env python
# -*- coding:utf-8 -*-
from base import BaseModel
from model.schema.demo_schema import DemoSchema

class DemoModel(BaseModel, DemoSchema):

    @classmethod
    def get_demo(cls, demo_id, **kwargs):
        """
        详情
        :return:
        :rtype:
        """
        # mongo
        fields = DemoSchema.fields()
        cls.insert({"uid": 102})
        d = cls.find_one({"uid": 102})

        # myqsl
        cls.mysql.insert(cls.collection, [{"name": 2}, {"name": 3}])
        data = cls.mysql.query_sql(sql="select * from demo where name=(name)", params={"name": 2})
        return cls._parse_data(fields)


    @classmethod
    def get_demo_by_spec(cls, spec, **kwargs):
        """
        详情
        :return:
        :rtype:
        """
        d = cls.find_one(spec)
        return cls._parse_data(d)


    @classmethod
    def get_demo_list_by_last_id(cls, last_id, count, **kwargs):
        """
        前端列表
        :return:
        :rtype:
        """
        spec = {}
        spec.update(kwargs.get("spec", {}))
        data_list, last_id = cls.find_list_by_last_id(spec,
                                                      count,
                                                      sort=[("create_at", -1), ],
                                                      fields=False,
                                                      last_id_field=False)
        return [cls._parse_data(d) for d in data_list if d], last_id

    @classmethod
    def get_demo_list_by_page(cls, page, count, **kwargs):
        """
        后台列表
        :return:
        :rtype:
        """
        spec = {}
        spec.update(kwargs.get("spec", {}))
        data_list, pages = cls.find_list_by_page(spec,
                                                 page,
                                                 count,
                                                 sort=[("create_at", -1), ],
                                                 fields=False)
        return [cls._parse_data(d) for d in data_list if d], pages

    @classmethod
    def create_demo(cls, *args, **kwargs):
        """
        创建
        :return:
        :rtype:
        """
        pass

    @classmethod
    def modify_demo(cls, *args, **kwargs):
        """
        修改
        :return:
        :rtype:
        """
        pass

    @classmethod
    def delete_demo(cls, demo_id, **kwargs):
        """
        删除
        :return:
        :rtype:
        """
        return cls.update({"_id": demo_id}, {"state": -1})

    @classmethod
    def _parse_data(cls, d, **kwargs):
        """
        组装单条数据
        :return:
        :rtype:
        """
        if not d:
            return {}

        d["demo_id"] = str(d.pop("_id", ""))

        return d


