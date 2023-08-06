
from distutils.core import setup, Extension

ext_modules = Extension(
    "web_server.Extension",
    include_dirs=["src"],
    sources=[
        "src/webserver_list.c",
        "src/webserver_rbtree.c",
        "src/webserver_alloc.c",
        "src/webserver_string.c",
        "src/webserver_urlcode.c",
        "src/webserver_base64.c",
        "src/webserver_uuid.c",
        "src/webserver_time.c",
        "src/webserver_conf.c",
        "src/webserver_logs.c",
        "src/webserver_fcgiapp.c",
        "src/webserver_request.c",
        "src/webserver_response.c",
        "src/webserver_upload.c",
        "src/webserver_session.c",
        "src/webserver_controller.c",
        "src/webserver.c",
    ])

py_modules = [
    "web_server.request",
    "web_server.response",
    "web_server.session",
    "web_server.bootstrap",
    "web_server.worker",
    "web_server.mysql_api",
    "web_server.druid_api",
]

install_requires = [
    "pymysql"
]

setup(
    name="wscode",
    version="1.2.1",
    author="lcgcode",
    author_email="15101629450@163.com",
    description="web-server",
    url="http://lcgcode.com/lcgcode/web-python",
    install_requires=install_requires,
    ext_modules=[ext_modules],
    py_modules=py_modules)


