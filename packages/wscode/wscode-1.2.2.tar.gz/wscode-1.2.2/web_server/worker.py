from .bootstrap import bootstrap
import web_server.Extension as Extension


def web_server_worker(fcgi):
    try:
        return bootstrap(fcgi).run()
    except Exception as e:
        Extension.log(str(e))


def run(): Extension.run(web_server_worker)

