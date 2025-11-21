import os
import sys


def get_secret(key, required=False, default=None):
    fn = os.path.join("/run/secrets/", key)
    if os.path.exists(fn):
        with open(fn, 'r') as fh:
            return fh.read()
    if key in os.environ:
        return os.environ[key]

    if required:
        print("ERROR: Missing secret '%s'" % key)
        sys.exit()
    else:
        return default
