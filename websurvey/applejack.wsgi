#!/usr/bin/env python

import os, sys
import site

VIRTUALENV = '/scratch2/www/software-quality-guidelines/websurvey'
site.addsitedir(VIRTUALENV + '/lib/python' + str(sys.version_info.major) + '.' + str(sys.version_info.minor) + '/site-packages')

SETTINGSDIR = '/scratch2/www/software-quality-guidelines/websurvey/websurvey' #<-- change this: the dir that holds your settings.py

if SETTINGSDIR not in sys.path:
    sys.path.append(SETTINGSDIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django import VERSION
if VERSION[0] == 1 and VERSION[1] < 7:
    import django.core.handlers.wsgi
    application = django.core.handlers.wsgi.WSGIHandler()
else:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()


