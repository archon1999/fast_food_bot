import os
import sys

import django


PACKAGE_PARENT = '..'
APP_DIR = os.path.join(PACKAGE_PARENT, 'app')
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(
        os.path.join(os.getcwd(), os.path.expanduser(__file__)),
    )
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
APP_DIR_PATH = os.path.normpath(os.path.join(SCRIPT_DIR, APP_DIR))
sys.path.append(APP_DIR_PATH)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

TOKEN = '1851468121:AAEoSjivgcFbopw55msL69oftY1ZOVWVWko'
