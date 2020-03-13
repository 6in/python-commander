from .. import ServiceBase
from bottle import Bottle, request, response, static_file, run, route, ServerAdapter
from gevent.pywsgi import WSGIServer
from praqta.interface import ApplicationContext, objdict, Row
from praqta.logger import Logger
from typing import Iterable, cast
import json
import services
from glob import glob
import os.path
import yaml

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

        super().route('/api/cmd/<command_name>',
                      ['GET'], self.get_command)
        super().route('/api/cmd/<command_name>',
                      ['POST'], self.post_command)
        super().route('/api/cmd', ['GET'], self.get_commands)

        super().route('/api/scripts', ['GET'], self.get_scripts)
        super().route('/api/scripts/<script>', ['GET'], self.get_script)
        super().route('/api/scripts/<script>', ['POST'], self.post_script)

        super().route('/api/db/<dbname>/query', ['POST'], self.db_query)
        super().route('/api/db/<dbname>/query_meta',
                      ['POST'], self.db_query_meta)
        super().route('/api/db/<dbname>/meta',
                      ['POST'], self.db_meta)
        super().route('/api/db/<dbname>/execute', ['POST'], self.db_execute)

        super().route('/',
                      ['GET'], self.index)

        super().route('/<file_path:path>',
                      ['GET'], self.static_controller)

        super().add_hook('after_request', self.enable_cors)

    def get_commands(self, **param):
        """
        commands配下のコマンドリストを返却
        """
        response.headers['Content-Type'] = 'application/json'

        ret = []
        for f in glob('./packages/commands/**/*.yml'):
            if f.endswith('template.yml'):
                continue
            with open(f, 'r') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                data = objdict(data)
                ret.append({
                    'name': data.name,
                    'comment': data.comment
                })
        ret = sorted(ret, key=lambda x: x['name'])
        return json.dumps(ret)

    def get_command(self, **param):
        response.headers['Content-Type'] = 'application/json'
        args = objdict(request.url_args)

        ret = {}
        basePath = os.path.abspath('./packages/commands')
        for ext in ['py', 'yml']:
            file = os.path.abspath(
                f'./packages/commands/{args.command_name}/{args.command_name}.{ext}')
            logger.info(f'read file={file}')
            if not file.startswith(basePath):
                response.status = 404
                return
            if not os.path.exists(file):
                response.status = 404
                return
            with open(file, 'r') as f:
                text = "".join(f.readlines())
                ret[ext] = text

        return json.dumps(ret)

    def post_command(self, **param):
        response.headers['Content-Type'] = 'application/json'
        json = objdict(request.json)

        args = objdict(request.url_args)
        json = objdict(request.json)

        for ext in ['py', 'yml']:
            file_name = os.path.abspath(
                f'./packages/commands/{args.command_name}/{args.command_name}.{ext}')

            if not file_name.startswith(os.path.abspath('./packages/commands/')):
                response.status = 404
                return

            # ファイル書き込み
            text = json.get(ext)
            with open(file_name, 'w') as f:
                f.write(text)

        return json.dump({})

    def get_scripts(self, **param):
        response.headers['Content-Type'] = 'application/json'

        ret = []
        for file in glob('./scripts/*.yml'):
            file = os.path.abspath(file)
            with open(file, 'r') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                data = objdict(data)
                (_, name) = os.path.split(file)
                ret.append({
                    'name': name,
                    'comment': data.comment
                })

        ret = sorted(ret, key=lambda x: x['name'])
        return json.dumps(ret)

    def get_script(self, **param):
        response.headers['Content-Type'] = 'application/json'
        args = objdict(request.url_args)

        ret = {}
        basePath = os.path.abspath('./scripts')
        file = os.path.abspath(
            f'./scripts/{args.script}')
        logger.info(f'read file={file}')
        if not file.startswith(basePath):
            response.status = 404
            return
        if not os.path.exists(file):
            response.status = 404
            return
        with open(file, 'r') as f:
            text = "".join(f.readlines())
            ret['script'] = text

        return json.dumps(ret)

    def post_script(self, **param):
        response.headers['Content-Type'] = 'application/json'

        args = objdict(request.url_args)
        json = objdict(request.json)

        file_name = args.script
        file_name = os.path.abspath(f'./scripts/{file_name}')

        if not file_name.startswith(os.path.abspath('./scripts')):
            response.status = 404
            return

        # ファイル書き込み
        text = json.script
        with open(file_name, 'w') as f:
            f.write(text)

        return json.dumps({})

    def db_query(self, **param):
        pass

    def db_query_meta(self, **param):
        pass

    def db_meta(self):
        pass

    def db_execute(self):
        pass

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

        parameters = {}
        if request.json:
            parameters = objdict(request.json).params

        parameters['script_file'] = args.script_file

        praqta.start(parameters)
        context = parameters['context']
        rows = []
        for row in context.get_rows():
            if type(row) == Row:
                row = row.raw()
            rows.append(row)

        return json.dumps(rows)


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
