#!C:\work\Python36-32\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'google-speech==1.0.15','console_scripts','google_speech'
__requires__ = 'google-speech==1.0.15'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('google-speech==1.0.15', 'console_scripts', 'google_speech')()
    )
