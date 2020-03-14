from praqta.interface import Row, objdict


class ArgSpec(object):
    def __init__(self, name: str, typeName: str, values: list, comment: str, require: bool, default):
        self.name = name
        self.type = typeName
        self.values = values
        self.comment = comment
        self.require = require
        self.default = default

    def get_value_type(self, value) -> str:
        dataType = type(value)
        if dataType == list:
            return 'list'

        if dataType == dict:
            return 'dict'

        if dataType == str:
            return 'string'

        if dataType == int:
            return 'bool'

        if dataType == bool:
            return 'bool'

        if dataType == object:
            return 'object'

    def validate(self, value) -> bool:

        if type(self.type) == str:
            self.check_type(self.type, value)

        if type(self.type) == list:

            # 許容するデータ型のリスト
            valueType = self.get_value_type(value)
            hint = ",".join(self.type)
            if not valueType in self.type:
                raise Exception(f'{self.name}のデータは {hint}いずれかのデータ型を指定ください。')

            self.check_type(valueType, value)

        return True

    def check_type(self, typeName: str, value: str):
        if typeName == 'enum':
            if not value in self.values:
                hint = ','.join(self.values)
                raise Exception(f'{self.name}の設定値は {hint}から選択してください。')

        if typeName == 'list':
            if type(value) != list:
                raise Exception(f'{self.name}の設定値は list型を指定してください。')

        if typeName in ['dict']:
            if not type(value) in [dict]:
                raise Exception(f'{self.name}の設定値は 辞書型を指定してください。')

        if typeName in ['object']:
            if not type(value) in [str, int, float, bool, dict, list, object]:
                raise Exception(f'{self.name}の設定値は 辞書型を指定してください。')

        if typeName == 'string':
            if type(value) != str:
                raise Exception(f'{self.name}の設定値は 文字列を指定してください。')

        if typeName == 'int':
            if not type(value) in [int, float]:
                raise Exception(f'{self.name}の設定値は、 数値を指定してください。')

        if typeName == 'bool':
            if type(value) != bool:
                raise Exception(f'{self.name}の設定値は、bool(yes/no)を指定してください。')
        return True


class ArgSpecs(object):
    def __init__(self, commandName):
        self.commandName = commandName
        self.specs = {}
        self.requires = []

    def append(self, spec: ArgSpec):
        if spec.require == True:
            self.requires.append(spec)
        self.specs[spec.name] = spec

    def validate(self, params):

        # パラメータ定義のrequire: noのデフォルト値を取得する
        defaultValue = {}
        for key in self.specs.keys():
            spec = self.specs[key]
            if spec.require == False:
                if not key in params:
                    params[key] = spec.default

        r = Row(params)

        # 必須プロパティチェック
        for v in self.requires:
            if r.get(v.name) == None:
                raise Exception(
                    f'{self.commandName}: {v.name}プロパティが設定されていません。')

        # パラメータのキーを取得
        for key in params.keys():
            # パラメータ仕様にないパラメータ
            if not key in self.specs:
                raise Exception(
                    f'{self.commandName}: {key}プロパティは、パラメータ仕様に定義されていません。')
            # 値を取得
            value = r.get(key)
            # 値のチェックを行う
            self.specs[key].validate(value)


def validate_spec(commandName: str, specDict: dict, logger) -> dict:
    spec = Row(specDict)
    if spec.get('name') == None:
        logger.error(f'{commandName}.yml: nameプロパティが定義されていません')

    if spec.get('comment') == None:
        logger.error(f'{commandName}.yml: commentプロパティが定義されていません')

    if spec.get('parameters') == None:
        logger.error(f'{commandName}.yml: parameterプロパティが定義されていません')

    if spec.get('sample') == None:
        logger.error(f'{commandName}.yml: sampleプロパティが定義されていません')

    ret = ArgSpecs(commandName)
    for name in spec.get('parameters').keys():
        param = Row(spec.get('parameters')[name])

        if param.get('type') == None:
            logger.error(f'{commandName}.yml: {name}.typeが指定されていません')

        checkTypes = []
        if type(param.get('type')) == str:
            checkTypes.append(param.get('type'))
        elif type(param.get('type')) == list:
            checkTypes = param.get('type')

        if len(checkTypes) > 0:
            for typeValue in checkTypes:
                if not typeValue in ['string', 'int', 'bool', 'enum', 'list', 'object', 'dict']:
                    logger.error(
                        f'{commandName}.yml: {name}.type は、string,int,bool,enum,list,dict,objectの何れかを指定してください')

        if param.get('type') == 'enum':
            if param.get('values') == None:
                logger.error(
                    f'{commandName}.yml: {name}.type がenumの時は、列挙値をvaluesに配列で記述してください')

        if param.get('comment') == None:
            logger.error(
                f'{commandName}.yml: {name}.comment が定義されていません。パラメータの説明を記述してください')

        if param.get('require') == None:
            logger.error(f'{commandName}.yml: {name}.require が定義されていません。')

        if param.get('default') == None:
            logger.error(f'{commandName}.yml: {name}.default が定義されていません。')

        ret.append(ArgSpec(name,
                           param.get('type'),
                           param.get('values'),
                           param.get('comment'),
                           param.get('require'),
                           param.get('default')))
    return ret
