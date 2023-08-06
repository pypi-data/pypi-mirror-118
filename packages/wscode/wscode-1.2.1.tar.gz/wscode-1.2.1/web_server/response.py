# -*- coding: utf-8 -*-

import json
import web_server.Extension as Extension


class response(dict):
    def __init__(self, fcgi):
        self.fcgi = fcgi
        self.header = {}
        self.content = ""
        self.buffer = ""

    def header_parse(self):
        if not self.header.get("Status"):
            self.buffer += "Status: 200\r\n"

        if not self.header.get("Content-Type"):
            self.buffer += "Content-Type: application/json\r\n"

        for key in self.header:
            self.buffer += key + ": " + self.header.get(key) + "\r\n"

        self.buffer += "\r\n"

    def content_parse(self):
        if self:
            try:
                self.content += json.dumps(self, ensure_ascii=False)
            except Exception as e:
                Extension.log(str(e))

        self.buffer += self.content

    def flush(self):
        self.header_parse()
        self.content_parse()
        Extension.response(self.fcgi, self.buffer)

    def CODE(self, code, msg):
        self["code"] = code
        self["msg"] = msg

    def OBJ(self, o):
        self.SUCCESS()
        self["data"] = o

    def LIST(self, o, total):
        self.SUCCESS()
        self["data"] = {
            "total": total,
            "list": o
        }

    def SUCCESS(self):
        return self.CODE(0, "成功")

    def SYSTEM_ERROR(self):
        return self.CODE(1000, "系统错误!")

    def SESSION_ERROR(self):
        return self.CODE(1001, "session错误!")

    def CONTROLLER_ERROR(self):
        return self.CODE(1002, "controller错误!")

    def LOGIN_ERROR(self):
        return self.CODE(1003, "登陆失败!")

    def PARAM_ERROR(self):
        return self.CODE(1004, "参数错误!")

    def NOT_DATA(self):
        return self.CODE(1005, "没有数据!")

