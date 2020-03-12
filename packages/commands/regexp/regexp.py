import typing
from .. import CommandBase
from praqta.interface import Row, CommandContext, objdict
from typing import cast
from logging import Logger
import re

logger = cast(Logger, {})


def parse_easy_regexp(pattern):
    return pattern


class RegExp(CommandBase):
    def __init__(self):
        """
        コンストラクタ
        メンバー変数の初期化をここで行います。
        """
        self.__has_data = True

    def init(self, context: CommandContext):
        """
        スクリプト読み込み後に、利用するコマンドの初期化時に呼び出れます。
        context.get_parameters()で、スクリプトに記述されたコマンドパラメータ
        を取得することができます。
        """
        # パラメータを取得する( self.__params.プロパティ名 でアクセス可能)
        self.__params = context.get_parameters()

        # 正規表現オプションを構築
        option = 0
        for opt in self.__params.match_options:
            if opt == 'verbose':
                option |= re.VERBOSE
            elif opt == 'multiline':
                option |= re.MULTILINE
            elif opt == 'dotall':
                option |= re.DOTALL
            elif opt == 'ignore':
                option |= re.IGNORECASE

        # 正規表現をコンパイルする
        reg = re.compile(parse_easy_regexp(
            self.__params.pattern), option)

        self.__reg = reg

    def proc(self, context: CommandContext):
        """
        メイン処理を行います。
        context.get_rows()を呼び出して、データ行を取得しながら、
        データ加工を行ってください。

        渡されてくるデータは、イテレータの場合もあるので、次に
        引き継ぐために、context.set_rows()で、データを引き渡してください。

        """
        # 正規表現取得
        reg = self.__reg
        # マッチングターゲットキーを取得
        target_key = self.__params.target_key
        # 結果格納用のキーを取得
        match_result_key = self.__params.match_result_key
        # 出力用のフィールド
        output = self.__params.output_keys

        # 次へ引き渡す行
        rows = []
        for row in iter(context.get_rows()):
            if type(row) == dict:
                row = dict(row)
            if type(row) == Row:
                row = dict(row.raw())

            # Rowラッパーに変換
            row = Row(row)
            row.set(match_result_key, False)
            # 検索対象文字列を取得
            line = row.get(target_key)
            if line == None:
                continue

            newRow = dict(output)

            # 正規表現マッチング
            pos = None
            matchResult = reg.match(line)
            if matchResult:
                # マッチ結果を保存
                row.set(match_result_key, True)

                # グループ1の発見場所を保存
                groups = matchResult.groups()
                if len(groups) > 0:
                    pos = matchResult.start(1)

                if len(groups) > 0:
                    # 正規表現のマッチング結果を、置換します。
                    if self.__params.extract_type == 'index':
                        for key in self.__params.group_key_map:
                            index = int(self.__params.group_key_map[key])
                            newRow[key] = groups[index-1]
                    else:
                        # ?Pで指定された正規表現のマッチ結果を抽出
                        d = matchResult.groupdict()
                        for key in d.keys():
                            newRow[key] = d[key]
            row.set('pos', pos)

            # 結果をマージ
            for key in newRow.keys():
                row.set(key, newRow.get(key))

            rows.append(row.raw())

        # 次のコマンドへ引渡し
        context.set_rows(rows)

    def term(self, context: CommandContext):
        """
        コマンド終了処理は、スクリプトの実行処理が終る直前に呼び出されます。
        initメソッド時にオープンしたリソースなどをクローズしてください
        """
        pass


def new_instance(loggerInject: Logger) -> CommandBase:
    global logger
    logger = loggerInject

    return RegExp()
