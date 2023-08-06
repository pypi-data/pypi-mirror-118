import json
import copy
import web_server.Extension as Extension


class session(dict):
    def __init__(self, request, response):
        self.request = request
        self.response = response
        self.sid = None
        self.old = {}
        self.parse()

    def parse(self):
        message = self.find()
        if message:
            self.update(message)
            self.old = copy.deepcopy(message)

    def create(self):
        try:
            self.sid = Extension.session_create(json.dumps(self))
            if self.sid:
                self.response.header["Set-Cookie"] = "sid=" + self.sid
        except Exception as e:
            Extension.log(str(e))

    def destroy(self):
        if self.sid:
            return Extension.session_destroy(self.sid)

    def find(self):
        try:
            self.sid = self.request.HTTP_COOKIE_DICT().get("sid")
            if self.sid:
                r = Extension.session_find(self.sid)
                if r:
                    return json.loads(r)
        except Exception as e:
            Extension.log(str(e))

        return {}

    def check(self):
        if self:
            return True

        if Extension.controller_check_pass(self.request.execution):
            return True

        self.response.SESSION_ERROR()
        return False

    def flush(self):
        if self.old != self:
            self.destroy()
            self.create()

