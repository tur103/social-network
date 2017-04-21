#!C:\work\Python36-32\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pytest==2.3.4','console_scripts','py.test-3.6'
__requires__ = 'pytest==2.3.4'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pytest==2.3.4', 'console_scripts', 'py.test-3.6')()
    )
