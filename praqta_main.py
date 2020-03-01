import sys
import importlib
# import praqta.praqta_engine as engine
from docopt import docopt

sys.path.append('./packages')


doc = """python-commander
usage:
    test.py [-h|--help] [-s|--scripts]

options:
    -h,--help       show this help message and exit
    -s <script>     script name  (optional)
"""


def main(args):

    engine = importlib.import_module('praqta.praqta_engine')
    # engine.main('config/properties.yml', 'sample.yml')
    engine.main('config/properties.yml', args['-s'])


if __name__ == '__main__':

    main(docopt(doc, version="0.0.1"))
