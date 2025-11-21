import json
from aitools.openaichatclient import OpenAIChatClient
import os
import sys
import time
from pydantic import BaseModel
from datetime import datetime
import hashlib
import pandas as pd
import pickle

from aitools.promptlibrary import ChatPromptModel

    
class Runnable():

    def __init__(self):
        pass

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

    def get_text_from_file(fn):
        if not os.path.exists(fn):
            raise Exception("File not found: %s" % fn)
        return open(fn).read()

class OpenAIChatRunnable(Runnable):

    def __init__(self, model, cache_dir, response_class):
        client = OpenAIChatClient(model = model)
        self.client = client
        self.response_class = response_class

        self.model = model
        #self.client_attrs_str = json.dumps(client_attrs, indent=4)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        self.cache_dir = cache_dir

    def _make_key_static(model, system_prompt, user_message):
        client_attrs = {
            "model": model,
        }
        client_attrs_str = json.dumps(client_attrs, indent=4)
        msg = client_attrs_str + "\n\n" + system_prompt + "\n\n" + user_message
        return hashlib.md5(msg.encode()).hexdigest()    
 
    def _make_key(self, system_prompt, user_message):
        return OpenAIChatRunnable._make_key_static(self.model, system_prompt, user_message)
        #msg = self.client_attrs_str + "\n\n" + system_prompt + "\n\n" + user_message
        #return hashlib.md5(msg.encode()).hexdigest()    
    
    def _get_fns(self, key):
        prompt_fn = os.path.join(self.cache_dir, f"{key}_prompt.txt")
        response_fn_json = os.path.join(self.cache_dir, f"{key}_response.json")
        response_fn_pkl = os.path.join(self.cache_dir, f"{key}_response.pkl")
        settings_fn = os.path.join(self.cache_dir, f"{key}_settings.json")
        return prompt_fn, response_fn_json, response_fn_pkl, settings_fn
    
    def load_json(self, fn):
        if os.path.exists(fn):
            with open(fn, "r") as f:
                return json.load(f)
        return None
    
    def save_json(self, fn, data):
        with open(fn, "w") as f:
            json.dump(data, f)
    
    def save_text(self, fn, text):
        with open(fn, "w") as f:
            f.write(text)
        print("Saved text to %s" % fn)

    def save_pickle(self, fn, data):
        with open(fn, "wb") as f:  # Note: using 'wb' for binary write
            pickle.dump(data, f)
        print("Saved pickle to %s" % fn)
      
    def load_pickle(self, fn):
        if os.path.exists(fn):
            with open(fn, "rb") as f:  # Note: using 'rb' for binary read
                return pickle.load(f)
        return None
    

    def get_cached_response(self, key):
        prompt_fn, response_fn_json, response_fn_pkl, settings_fn = self._get_fns(key)
        print("Prompt fn: %s" % prompt_fn)
        if os.path.exists(response_fn_pkl):
            model = self.load_pickle(response_fn_pkl)
            return model
        elif os.path.exists(response_fn_json):
            response = self.load_json(response_fn_json)
            model = self.response_class.model_validate(response)
            return model
        else:
            return None
        
 
    def save_files(self, key, system_prompt, user_message, settings, response):
        prompt_fn, response_fn_json, response_fn_pkl, settings_fn = self._get_fns(key)

        prompt_text = system_prompt + "\n\n" + user_message
        self.save_text(prompt_fn, prompt_text)

        settings_str = json.dumps(settings, indent=4)
        self.save_text(settings_fn, settings_str)

        try:
            response_dict = response.model_dump()
            response_str = json.dumps(response_dict, indent=4)
            self.save_text(response_fn_json, response_str)
        except Exception as e:
            self.save_pickle(response_fn_pkl, response)

    def _get_key_static(model, input_model):
        system_prompt = input_model.system_prompt
        user_message = input_model.user_message
        params = input_model.params
        user_message = Runnable._replace_params(user_message, params)
        return OpenAIChatRunnable._make_key_static(model, system_prompt, user_message)
    
    def execute(self, input_model, sleep_on_cache_miss=2, skip_cache=False, override_cache_key=None):

        assert isinstance(input_model, ChatPromptModel), f"Expected input_pydantic_model to be of type ChatPromptModel, got {type(input_model)}"

        system_prompt = input_model.system_prompt
        user_message = input_model.user_message
        params = input_model.params
        user_message = OpenAIChatRunnable._replace_params(user_message, params)

        if override_cache_key is not None:
            key = override_cache_key
        else:
            key = self._make_key(system_prompt, user_message)

        # Check old cache key first
        # response = self.get_cached_response(orig_key)
        # if response is not None:

        if not skip_cache:
            response = self.get_cached_response(key)
            if response is not None and not skip_cache:
                print("Cache Hit: %s" % key)
                return key, response

        print("Cache Miss")
        print("Key: %s" % key)
        #sys.exit()
        print("\nSystem Prompt:")
        print(system_prompt)
        print("\nUser Message:")
        print(user_message)

        (settings, response) = self.client.generate_model(system_prompt, user_message, model_class=self.response_class)
        if response is None:
            print("Error generating model")
            return None, None
        
        print("\nResponse:")
        print(response.model_dump())
        print("Type of response: ", type(response))

        self.save_files(key, system_prompt, user_message, settings, response)

        print("Sleeping %s seconds" % sleep_on_cache_miss)
        time.sleep(sleep_on_cache_miss)
        return key, response
    
