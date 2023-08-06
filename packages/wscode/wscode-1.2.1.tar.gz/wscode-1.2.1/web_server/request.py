import json
import web_server.Extension as Extension


class request(dict):
    def __init__(self, fcgi):
        self.fcgi = fcgi
        self.method = self.REQUEST_METHOD()
        self.execution = self.EXECUTION()
        self.content_type = self.CONTENT_TYPE()
        self.content_body = None
        self.parse()

    def get_param(self, key):
        return Extension.request_param(self.fcgi, key)

    def REQUEST_METHOD(self):
        return self.get_param("REQUEST_METHOD")

    def DOCUMENT_URI(self):
        return self.get_param("DOCUMENT_URI")

    def EXECUTION(self):
        return Extension.request_execution(self.fcgi)

    def QUERY_STRING(self):
        return self.get_param("QUERY_STRING")

    def QUERY_STRING_DICT(self):
        return Extension.request_query_string_dict(self.fcgi)

    def CONTENT_TYPE(self):
        return self.get_param("CONTENT_TYPE")

    def REMOTE_ADDR(self):
        return self.get_param("REMOTE_ADDR")

    def HTTP_COOKIE(self):
        return self.get_param("HTTP_COOKIE")

    def HTTP_COOKIE_DICT(self):
        return Extension.request_http_cookie_dict(self.fcgi)

    def HTTP_ORIGIN(self):
        return self.get_param("HTTP_ORIGIN")

    def CONTENT_LENGTH(self):
        return Extension.request_content_length(self.fcgi)

    def CONTENT_BODY(self):
        return Extension.request_content_body(self.fcgi)

    def UPLOAD(self):
        return Extension.request_upload(self.fcgi)

    def parse(self):
        if self.method == "GET":
            self.get_parse()
        elif self.method == "POST":
            self.post_parse()

    def get_parse(self):
        try:
            self.update(self.QUERY_STRING_DICT())
        except Exception as e:
            Extension.log(str(e))

    def post_parse(self):
        if "json" in self.content_type:
            self.json_parse()
        elif "form-data" in self.content_type:
            self.update_parse()
        else:
            self.content_body = self.CONTENT_BODY()

    def json_parse(self):
        try:
            self.content_body = self.CONTENT_BODY()
            data = json.loads(self.content_body)
            if type(data) == dict:
                self.update(data)

            if type(data) == list:
                self.update({
                    "list": data
                })

        except Exception as e:
            Extension.log(str(e))

    def update_parse(self):
        try:
            self["UPLOAD"] = self.UPLOAD()
        except Exception as e:
            Extension.log(str(e))

