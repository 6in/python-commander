from .. import ServiceBase
from bottle import Bottle, request, response, static_file, run, route, ServerAdapter
from gevent.pywsgi import WSGIServer
from praqta.interface import ApplicationContext
from praqta.interface import objdict
from praqta.logger import Logger
from typing import Iterable, cast
import json
import services

logger = cast(Logger, None)


class SSLWebServer(ServerAdapter):
    cert_file = ""

    @staticmethod
    def set_certfile(file: str):
        SSLWebServer.cert_file = file

    def run(self, handler):
        srv = WSGIServer((self.host, self.port), handler,
                         certfile=SSLWebServer.cert_file,
                         keyfile=SSLWebServer.cert_file)
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

        super().add_hook('after_request', self.enable_cors)

    def enable_cors(self):

        # CORSのヘッダ取得
        cors_headers = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token '
        # cors_headers += app.cors_headers

        origin = "*"
        # if 'Origin' in request.headers().keys():
        #     origin = request.headers()['Origin']

        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, UPDATE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = cors_headers
        # クッキー対応
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        # 24時間のキャッシュ
        response.headers['Access-Control-Max-Age'] = '86400'

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
            param = {
                "host": self.__config.host,
                "port": self.__config.port,
                "debug": self.__config.debug,
                "reloader": True,
            }
            if self.__config.ssl:
                SSLWebServer.set_certfile(self.__config.key_file)
                param["server"] = SSLWebServer

            self.__bottle.run(**param)

        finally:
            pass

    def stop(self, context: dict):
        pass


def new_instance(loggerInject: Logger) -> ServiceBase:
    global logger
    logger = loggerInject
    return HttpService()
