

import os
import json

def get_secret(key, dir=None):

    def read_file(fn):
        with open(fn, 'r') as f:
            return f.read().strip()

    def try_parse_json(myjson):
        try:
            json_object = json.loads(myjson)
            return json_object
        except ValueError as e:
            return None
    
    """
    Retrieves a secret from a secrets file.
    """

    # Check for the secret like we are in a Render.com environment.
    dirs = [
        '/etc/secrets', # docker environment
        '../.secrets', # local virtual environment
        '../../.secrets' # local virtual environment
    ]

    if dir is not None:
        dirs = [dir]

    for dir in dirs:
        fn = os.path.join(dir, key)
        #print("Checking for secret in %s" % fn)
        if os.path.exists(fn):
            secret = read_file(fn)
            json_obj = try_parse_json(secret)
            if json_obj is not None:
                return json_obj
            else:
                return secret


    print("ERROR: Secret '%s'not found." % key)
    return None
