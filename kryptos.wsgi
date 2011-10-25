import os
import sys
import site
# redirect stdout to stderr because of limitations of wsgi
sys.stdout = sys.stderr

# append project dir to path
PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
vepath = PROJ_DIR + '/../venv/lib/python2.7/site-packages'

site.addsitedir(vepath)

sys.path.append(PROJ_DIR)
sys.path.append(os.path.join(PROJ_DIR, '..'))

prev_sys_path = list(sys.path)

new_sys_path = [p for p in sys.path if p not in prev_sys_path]
for item in new_sys_path:
    sys.path.remove(item)
sys.path[:0] = new_sys_path

os.environ['DJANGO_SETTINGS_MODULE'] = 'crypt_app.settings'
os.environ['SETTINGS_MODULE'] = 'crypt_app.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


