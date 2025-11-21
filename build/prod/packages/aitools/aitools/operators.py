import os
import json
import time
import hashlib
from aitools.promptlibrary import ChatPromptModel
from aitools.runnables import OpenAIChatRunnable
from aitools import OpenAIChatClient



class BaseOperator():

    def __init__(self, open_ai_model, response_output_dir, system_prompt, response_class, sleep_on_cache_miss=2):
        self.open_ai_model = open_ai_model
        if not os.path.exists(response_output_dir):
            os.makedirs(response_output_dir)
        self.response_output_dir = response_output_dir
        #self.cache_dir = cache_dir
        #self.key = output_key
        self.system_prompt = system_prompt
        self.response_class = response_class
        self.sleep_on_cache_miss = sleep_on_cache_miss


    def _get_output_fn(self, key):
        return f"{self.response_output_dir}/{key}.json"

    def _save_output_model(self, key, model):
        fn = self._get_output_fn(key)
        with open(fn, "w") as f:
            json.dump(model.model_dump(), f, indent=4)

    def _load_output_model(self, key):
        fn = self._get_output_fn(key)
        if not os.path.exists(fn):
            return None
        with open(fn, "r") as f:
            return self.response_class(**json.load(f))
        
    def _is_done(self, key):
        return os.path.exists(self._get_output_fn(key))

    def _replace_params(text, params):
        for k,v in params.items():
            #print("Key: %s, Value is type: %s" % (k, type(v)))
            if type(v) == str:
                v_str = v
            else:
                v_str = json.dumps(v, indent=4)
            text = text.replace("{%s}" % k, v_str)
        params_str = json.dumps(params, indent=4)
        text = text.replace("{__all__}", params_str)
        return text

    def hash_string(self, s):
        return hashlib.md5(s.encode()).hexdigest()


    def run(self, key, user_prompt, params, skip_cache=False, debug=True):

        if self._is_done(key) and not skip_cache:
            print(f"Loading {key} from cache")
            return key, self._load_output_model(key)

        print("Cache Miss for %s" % key)

        client = OpenAIChatClient(model = self.open_ai_model)

        user_message = BaseOperator._replace_params(user_prompt, params)

        print("System Prompt:")
        print(self.system_prompt)

        print("User Message:")
        print(user_message)

        (settings, response) = client.generate_model(self.system_prompt, user_message, model_class=self.response_class)
        if response is None:
            print("Error generating model")
            return None, None
        
        print("\nResponse:")
        print(response.model_dump())
        print("Type of response: ", type(response))

        self._save_output_model(key, response)

        # self.save_files(key, system_prompt, user_message, settings, response)

        print("Sleeping %s seconds" % self.sleep_on_cache_miss)
        time.sleep(self.sleep_on_cache_miss)
        # return key, response
        return key, response

