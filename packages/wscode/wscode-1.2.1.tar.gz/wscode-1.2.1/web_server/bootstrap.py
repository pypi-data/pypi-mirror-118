import json
from .request import request
from .response import response
from .session import session
from .mysql_api import mysql_api
from .druid_api import druid_api
import web_server.Extension as Extension


class bootstrap:
    def __init__(self, fcgi):
        self.request = request(fcgi)
        self.response = response(fcgi)
        self.session = session(self.request, self.response)
        self.db = mysql_api(
            Extension.get_conf("mysql", "host"),
            Extension.get_conf("mysql", "user"),
            Extension.get_conf("mysql", "pass"),
            Extension.get_conf("mysql", "db"))
        self.druid = druid_api(
            Extension.get_conf("druid", "url"),
            Extension.get_conf("druid", "table"))

    def controller(self):
        controller_run = Extension.get_controller(self.request.execution)
        if not controller_run:
            return self.response.CONTROLLER_ERROR()

        try:
            controller_run(self, self.request, self.response, self.session)
        except Exception as e:
            Extension.log(str(e))
            return self.response.SYSTEM_ERROR()

        if not self.response and not self.response.content:
            return self.response.NOT_DATA()

    def run(self):
        if self.session.check():
            self.controller()
        self.session.flush()
        self.response.flush()
        self.log()

    def log(self):
        try:
            Extension.log(json.dumps({
                "execution": self.request.execution,
                "request": self.request,
                "response": self.response,
                "session": self.session,
                }, ensure_ascii=False))
        except Exception as e:
            Extension.log(str(e))

