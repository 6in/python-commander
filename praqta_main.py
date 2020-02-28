import sys
import praqta.praqta_engine as engine
from docopt import docopt

doc = """python-commander
usage:
    test.py [-h|--help] [-s|--scripts]

options:
    -h,--help       show this help message and exit
    -s <script>     script name  (optional)
"""

if __name__ == '__main__':

    args = docopt(doc, version="0.0.1")

    # engine.main('config/properties.yml', 'sample.yml')
    engine.main('config/properties.yml', args['-s'])
