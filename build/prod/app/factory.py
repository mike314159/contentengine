from utils.secrets_store import get_secret
#from blueskyclient import BlueskyClient

class ObjectFactory:

    def __init__(self):
        self.objs = {}

    BLUESKY_CLIENT = "bluesky_client"


    def get_obj(self, obj_name):

        if obj_name in self.objs:
            return self.objs[obj_name]

        # if obj_name == ObjectFactory.BLUESKY_CLIENT:
        #     bluesky_config = get_secret("bluesky")
        #     client = BlueskyClient(bluesky_config["username"], bluesky_config["password"])
        #     self.objs[obj_name] = client
        #     return client
