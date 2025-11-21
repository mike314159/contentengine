import os

# This is a helper class to rturn consistent information about the app
# that we can use in logging, etc. 

# It is designed to work in local container environments as well 
# as production cloud (such as Render.com) environments.

class DeploymentInfo:
    def __init__(self):
        pass

    def get_app_env(self):
        
        # Render.com sets two environment variables that we can use to
        # RENDER=true
        # RENDER_SERVICE_ID=srv-cou3o7q0si5c7397tjg0
        
        UNKNOWN_STR = 'unknown'

        # Environment variables set by Render.com
        # RENDER=true 
        render = os.getenv("RENDER", None)
        if render == "true":
            deployment = "render"
            hostname = os.getenv("RENDER_SERVICE_ID", UNKNOWN_STR)
            env = 'prod'
        else:
            # CONTAINER_ENV will be set when running container locally with peach.py
            env = os.getenv("CONTAINER_ENV", None)
            if env is not None:
                deployment = "local"
                hostname = os.getenv("HOSTNAME", UNKNOWN_STR)
            else:
                # If all else fails, we are running locally in a non-container environment
                deployment = 'local_venv'
                hostname = os.getenv("HOSTNAME", UNKNOWN_STR)
                env = 'dev'

        return {
            "deployment": deployment,
            "host": hostname,
            "env": env
        }
    
    def get_env(self):
        return self.get_app_env()["env"]

    def is_local_deployment(self):
        info = self.get_app_env()
        return info["deployment"] == "local"

    def is_local_venv(self):
        info = self.get_app_env()
        return info["deployment"] == "local_venv"

    def is_not_production(self):
        return self.get_env() != "prod"

    def is_production(self):
        return self.get_env() == "prod"
