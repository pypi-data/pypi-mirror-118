
import importlib
import web_server.Extension as Extension


def controller(execution, bootstrap, request, response, session):
    try:
        module = importlib.import_module(execution)
        module.run(bootstrap, request, response, session)
        return True
    except ModuleNotFoundError as e:
        return Extension.log(str(e))
    except Exception as e:
        return Extension.log(str(e))
    return False
