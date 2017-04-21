#!C:\work\Python36-32\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'thread==0.1.0','console_scripts','thread'
__requires__ = 'thread==0.1.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('thread==0.1.0', 'console_scripts', 'thread')()
    )
