"""
WSGI config for dtop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys
HERE = os.path.dirname(__file__)
sys.path.append(HERE)
sys.path.append(os.path.dirname(HERE))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtop.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()