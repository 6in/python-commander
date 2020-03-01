

from praqta.interface import objdict
from .. import ServiceBase
from praqta.interface import ApplicationContext
from bottle import Bottle, request, response, static_file, run, route, ServerAdapter
from gevent.pywsgi import WSGIServer

import services
import json


class SSLWebServer(ServerAdapter):

    def run(self, handler):
        srv = WSGIServer((self.host, self.port), handler,
                         certfile='./config/server.pem',
                         keyfile='./config/server.pem')
        srv.serve_forever()


class BottleApp(Bottle):
    def __init__(self, parameters: dict):
        super().__init__()
        self.__parameters = objdict(parameters)
        self.init_route()

    def init_route(self):
        super().route('/api/execute/<script_file>',
                      ['GET'], self.execute_script)
        super().route('/',
                      ['GET'], self.index)
        super().route('/<file_path:path>',
                      ['GET'], self.static_controller)

    def index(self, **param):
        return static_file(
            'index.html',
            root=self.__parameters.static_root)

    def static_controller(self, **param):
        args = objdict(request.url_args)
        return static_file(
            args.file_path,
            root=self.__parameters.static_root)

    def execute_script(self, **param):
        response.headers['Content-Type'] = 'application/json'

        args = objdict(request.url_args)
        praqta = services.get_service('praqta')[0]

        parameters = {
            "script_file": args.script_file
        }
        praqta.start(parameters)
        context = parameters['context']
        ret = [x.raw() for x in context.get_rows()]
        return json.dumps(ret)


class HttpService(ServiceBase):
    def init(self, config: dict):
        self.__config = objdict(config)
        self.__bottle = BottleApp(config)

    def start(self, context: dict):
        try:
            self.__bottle.run(
                host=self.__config.host,
                port=self.__config.port,
                debug=True,
                reloader=True,
                # server=SSLWebServer
            )
        finally:
            pass

    def stop(self, context: dict):
        pass


def new_instance() -> ServiceBase:
    return HttpService()
