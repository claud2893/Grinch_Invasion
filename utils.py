import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # When packaged by PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")  # When running directly

    return os.path.join(base_path, relative_path)