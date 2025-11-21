

import os
import random
import json
import sys
import re
import time
import datetime
from openai import OpenAI
#from utils.secrets_store import get_secret
import hashlib


class OpenAIPydanticClient:



    def __init__(self, openai_api_key, model = "gpt-4o", cache_dir=None, skip_saving_attrs=False):
        self.model = model
        self.client = OpenAI(
            #temperature=temperature, 
            api_key=openai_api_key, 
            #model_name=model_name
        )
        self.cache_dir = cache_dir
        if cache_dir is not None:
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
            self.cache_dir = cache_dir
        self.skip_saving_attrs = skip_saving_attrs

    def generate(self, system_prompt, user_message, model_class, sleep_time=None):

        print("\nSystem prompt:\n", system_prompt)
        print("User message:\n", user_message)
        print("Model class: ", model_class)

        try:
            completion = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
                response_format=model_class,
            )

            response = completion.choices[0].message.parsed
            print("Response: ", response)
            #sys.exit()
            if sleep_time is not None:
                print("Sleeping for %d seconds" % sleep_time)
                time.sleep(sleep_time)
            return response
        except Exception as e:
            print("Error generating model: %s" % e)
            return None
    

    #--------------------------------
    # Caching Related Functions
    #--------------------------------

    def _get_fn(self, key, override_cache_dir=None):
        if override_cache_dir is not None:
            cache_dir = override_cache_dir
        else:
            cache_dir = self.cache_dir
        #input_fn = f'''{cache_dir}/{key}_input.json'''
        response_fn = f'''{cache_dir}/{key}.json'''
        return response_fn

    def _make_cache_key(self, input_attrs):
        attrs_str = json.dumps(input_attrs, indent=4)
        return hashlib.md5(attrs_str.encode()).hexdigest()       

    def _load_response_from_file(self, fn, model_class):
        if os.path.exists(fn):
            with open(fn, "r") as f:
                json_data = f.read()  # This reads the string
                response_json = json.loads(json_data)  # Parse the JSON string
                try:
                    return model_class(**response_json)  # Now response_json is a dict
                except:
                    print("Error parsing response json")
                    print(response_json)
                    return None
        return None

    def _save_dict_to_file(self, fn, data):
        with open(fn, "w") as f:
            json.dump(data, f, indent=4)

    def _save(self, response_fn, response):
        #if not self.skip_saving_attrs:
        #    self._save_dict_to_file(fn, input_attrs)
        response_dict = response.model_dump()
        self._save_dict_to_file(response_fn, response_dict)

    def is_cached(self, key, override_cache_dir=None):
        response_fn = self._get_fn(key, override_cache_dir)
        return os.path.exists(response_fn)

    def get_cached_response(self, key, model_class, override_cache_dir=None):
        response_fn = self._get_fn(key, override_cache_dir)
        return self._load_response_from_file(response_fn, model_class)

    def generate_use_cache(self, system_prompt, user_message, model_class, 
                           key=None, sleep_time=10, force_refresh=False, 
                           disable_refresh=False, override_cache_dir=None):

        input_attrs = {
            "model": self.model,
            "response_type": "model",
            "model_class": model_class.__name__
        }
        if key is None:
            key = self._make_cache_key(input_attrs)

        response_fn = self._get_fn(key, override_cache_dir)
        #print("Response filename: ", response_fn)
        is_cached = os.path.exists(response_fn)

        if is_cached and not force_refresh:
            print("Loading response from cache: ", response_fn)
            model = self._load_response_from_file(response_fn, model_class)
            if model is not None:
                return model
            else:
                print("Invalid cached response, generate new response")

        if disable_refresh:
            print("Skipping OpenAI call, refresh disabled")
            return None

        print("Calling OpenAI, Generating new response...")
        response = self.generate(system_prompt, user_message, model_class, sleep_time=sleep_time)

        self._save(response_fn, response)

        return response