"""
WSGI config for quran_cl project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""
import os
import sys

os.chdir(os.path.abspath(os.path.dirname(__file__) + "/.."))
sys.path.insert(0, os.getcwd())
activate_this_file = os.path.abspath(os.path.dirname(__file__) + "/../pyenv/bin/activate_this.py")
execfile(activate_this_file, dict(__file__=activate_this_file))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quran_cl.settings")

application = get_wsgi_application()
