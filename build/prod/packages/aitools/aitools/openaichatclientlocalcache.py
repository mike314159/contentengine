
import os
import random
import json
import sys
import re
import time
import datetime
import hashlib
from openai import OpenAI
from aitools.openaichatclient import ChatMessage, OpenAIChatClient
from utils.secrets_store import get_secret




class OpenAIClientWithLocalCache:

    #def __init__(self, cache_dir, model="gpt-3.5-turbo-1106"):
    def __init__(self, cache_dir, open_ai_client):
        self.client = open_ai_client
        self.data_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)

    def new_from_config(config):
        cache_dir = config['cache_dir']
        openai_api_key = config['api_key']
        model = config['model']
        open_ai_client = OpenAIChatClient(openai_api_key, model)
        return OpenAIClientWithLocalCache(cache_dir, open_ai_client)

    def _load_json_from_file(self, fn):
        with open(fn, "r") as f:
            return json.load(f)
        
    def _load_text_from_file(self, fn):
        print("Loading text from file: ", fn)
        with open(fn, "r") as f:
            return f.read()

    def _save_json_to_file(self, fn, data):
        if data is None:
            return
        json_str = json.dumps(data, indent=4)
        with open(fn, "w") as f:
            f.write(json_str)
        print("Saved response to file: ", fn)
        
    def _save_text_to_file(self, fn, text):
        with open(fn, "w") as f:
            f.write(text)
        print("Saved response to file: ", fn)

    def _get_fn(self, key, response_type):
        #response_fn = f'''{self.data_dir}/{key}.json'''
        if response_type == OpenAIChatClient.RESPONSE_TYPE_STR:
            response_fn = os.path.join(self.data_dir, f"{key}.txt")
        elif response_type == OpenAIChatClient.RESPONSE_TYPE_LIST:
            response_fn = os.path.join(self.data_dir, f"{key}.json")
        elif response_type == OpenAIChatClient.RESPONSE_TYPE_DICT:
            response_fn = os.path.join(self.data_dir, f"{key}.json")
        else:
            assert False, "Invalid response format: %s" % response_type

        prompt_fn = f'''{self.data_dir}/{key}_prompt.txt'''
        settings_fn = f'''{self.data_dir}/{key}_settings.json'''
        return (settings_fn, prompt_fn, response_fn)
    
    def _load_response_from_file(self, fn, response_type):
        if response_type == OpenAIChatClient.RESPONSE_TYPE_STR:
            return self._load_text_from_file(fn)
        else:
            return self._load_json_from_file(fn)

    def _save_response_to_file(self, fn, response, response_type):
        if response_type == OpenAIChatClient.RESPONSE_TYPE_STR:
            self._save_text_to_file(fn, response)
        else:
            self._save_json_to_file(fn, response)

    def in_cache(self, key):
        (settings_fn, prompt_fn, response_fn) = self._get_fn(key)
        return os.path.exists(response_fn)

    def strip_invalid_json_chars(json_string):
        # Use regular expressions to find the first and last valid JSON characters
        match = re.search(r'[\[{]', json_string)
        if match:
            start = match.start()
        else:
            return None  # No valid JSON structure found
        
        match = re.search(r'[\]}]', json_string[::-1])
        if match:
            end = len(json_string) - match.start()
        else:
            return None  # No valid JSON structure found
        
        # Return the cleaned JSON string
        return json_string[start:end]
    
    def _make_cache_key(self, system_prompt, user_message, expected_response_type):
        model = self.client.model
        attrs = {
            "model": model,
            "system_prompt": system_prompt,
            "user_message": user_message,
            "expected_response_type": expected_response_type,
        }
        attrs_str = json.dumps(attrs, indent=4)
        return hashlib.md5(attrs_str.encode()).hexdigest()    
 

    def generate(self, prompt, expected_response_type, sleep_time=1, cache_key=None, disable_cache=False):

        if cache_key is None:
            # Generate a key from the prompt
            cache_key = self._make_cache_key(prompt, expected_response_type)

        (settings_fn, prompt_fn, response_fn) = self._get_fn(cache_key, expected_response_type)
        if os.path.exists(response_fn) and not disable_cache:
            print("Loading response from cache: ", response_fn)
            response = self._load_response_from_file(response_fn, expected_response_type)
            return response
    
        # if not enable_call_open_ai:
        #     print("Skipping OpenAI call for key: ", cache_key)
        #     return None
        
        print("Calling OpenAI, Generating new response...")
        print("Prompt: ", prompt)
        settings = {
            "model": self.client.model,
            "response_format": expected_response_type,
            "timestamp": datetime.datetime.now().isoformat()
        }

        messages = [
            ChatMessage(role="system", content=prompt),
        ]

        (settings, response) = self.client.generate(messages, expected_response_type, sleep_time=None)

        # if expected_response_type == OpenAIChatClient.RESPONSE_TYPE_STR:
        #     try:
        #         response_message = CachingOpenAIClient.strip_invalid_json_chars(response_message)
        #         response = json.loads(response_message)
        #     except:
        #         print("Error parsing response json")
        #         print(response_message)
        #         response = None
        # else:
        #     response = response_message

        # #print("Response: ", response)

        # if response_format == 'html':
        #     response = response.replace('\n', '')
        #     first_char = response.find('<')
        #     if first_char != -1:
        #         response = response[first_char:]
        #     last_char = response.rfind('>')
        #     if last_char != -1:             
        #         response = response[:last_char+1]

        # data = {
        #     "prompt": prompt,
        #     "response": response
        # }

        self._save_response_to_file(response_fn, response, expected_response_type)
        self._save_text_to_file(prompt_fn, prompt)  # Save prompt
        self._save_json_to_file(settings_fn, settings)  # Save settings

        if sleep_time is not None:
            #sleep_time = random.randint(5, 10)
            print("Sleeping for %d seconds" % sleep_time)
            time.sleep(sleep_time)
        return (settings, response)



    def generate_text(self, system_prompt, user_message, cache_key=None, disable_cache=False):

        expected_response_type = OpenAIChatClient.RESPONSE_TYPE_STR
        if cache_key is None:
            cache_key = self._make_cache_key(system_prompt, user_message, expected_response_type)

        settings = {
            "model": self.client.model,
            "response_format": expected_response_type,
            "timestamp": datetime.datetime.now().isoformat()
        }

        (settings_fn, prompt_fn, response_fn) = self._get_fn(cache_key, expected_response_type)
        if os.path.exists(response_fn) and not disable_cache:
            print("Loading response from cache: ", response_fn)
            response = self._load_response_from_file(response_fn, expected_response_type)
            return (settings, response)
        
        print("Calling OpenAI, Generating new response...")
        prompt = f'''System:\n{system_prompt}\n\nUser:\n{user_message}'''
        print("Prompt: ", prompt)

        (settings, response) = self.client.generate_text(system_prompt=system_prompt, user_message=user_message)

        self._save_response_to_file(response_fn, response, expected_response_type)
        self._save_text_to_file(prompt_fn, prompt)  # Save prompt
        self._save_json_to_file(settings_fn, settings)  # Save settings

        return (settings, response)