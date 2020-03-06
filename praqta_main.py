import sys
import importlib
# import praqta.praqta_engine as engine
from docopt import docopt

sys.path.append('./packages')


doc = """python-commander
usage:
    praqta_main.py (-c|--config <config> ) [-s|--script <script>] [-p <params>...]

options:
    -h,--help       show this help message and exit
    -c --config     config path
    -s --script     script name  (optional)
    -p              args key value
"""


def main(args):

    engine = importlib.import_module('praqta.praqta_engine')
    engine.main(
        args['<config>'],
        args['<script>'],
        args['<params>'])


if __name__ == '__main__':

    main(docopt(doc, version="0.0.1"))
