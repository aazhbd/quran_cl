#!/usr/bin/env python
import os
import sys

os.chdir(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.getcwd())
activate_this_file = os.path.abspath(os.path.dirname(__file__) + "/pyenv/bin/activate_this.py")
execfile(activate_this_file, dict(__file__=activate_this_file))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quran_cl.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
