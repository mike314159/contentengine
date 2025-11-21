
from aitools.runnables import *
from aitools.promptlibrary import PromptLibrary, ChatPromptModel
from aitools.operators import BaseOperator
import hashlib
import pandas as pd
import json
import time
import os
import datetime
import requests
from utils.secrets_store import get_secret


'''
Example response

Calling Perplexity API
{
    "id": "a489b1d3-dab4-44d3-9abe-2e87d3340c62",
    "model": "sonar-pro",
    "created": 1755370581,
    "usage": {
        "prompt_tokens": 13,
        "completion_tokens": 112,
        "total_tokens": 125,
        "search_context_size": "low",
        "cost": {
            "input_tokens_cost": 0.0,
            "output_tokens_cost": 0.002,
            "request_cost": 0.006,
            "total_cost": 0.008
        }
    },
    "citations": [
        "https://www.britannica.com/place/France",
        "https://www.instagram.com/p/DNVdq3aowxk/",
        "https://www.britannica.com/place/Paris",
        "https://www.instagram.com/reel/DNMW7tny54-/",
        "https://www.cometoparis.com/visit-paris-c9000724"
    ],
    "search_results": [
        {
            "title": "France | History, Maps, Flag, Population, Cities, Capital, & ...",
            "url": "https://www.britannica.com/place/France",
            "date": "2025-08-12",
            "last_updated": "2025-08-16"
        },
        {
            "title": "Paris,\u2764 the capital of France, is a world-famous city known for its ...",
            "url": "https://www.instagram.com/p/DNVdq3aowxk/",
            "date": "2025-08-14",
            "last_updated": null
        },
        {
            "title": "Paris | Definition, Map, Population, Facts, & History",
            "url": "https://www.britannica.com/place/Paris",
            "date": "2025-08-12",
            "last_updated": "2025-08-16"
        },
        {
            "title": "Paris, the capital of France, is renowned as a global ... - Instagram",
            "url": "https://www.instagram.com/reel/DNMW7tny54-/",
            "date": "2025-08-10",
            "last_updated": null
        },
        {
            "title": "Visiting Paris in 2025: What to Do, What to See, Itineraries, ...",
            "url": "https://www.cometoparis.com/visit-paris-c9000724",
            "date": "2025-08-10",
            "last_updated": "2025-06-28"
        }
    ],
    "object": "chat.completion",
    "choices": [
        {
            "index": 0,
            "finish_reason": "stop",
            "message": {
                "role": "assistant",
                "content": "The capital of France is **Paris**[1][2][3][4][5].\n\nParis is not only the political center of France but also a major global city renowned for its culture, history, and influence in areas such as fashion, gastronomy, and the arts[1][3][4]. The city, often referred to as the \"City of Light,\" sits on the River Seine in the north-central part of the country and is widely regarded as one of the world's most important and attractive urban centers[2][3][5]."
            },
            "delta": {
                "role": "assistant",
                "content": ""
            }
        }
    ]
}
'''



class PerplexityClient():

    def __init__(self):
        self.perplexity_api_key = get_secret("perplexity_api_key")

    def get_payload_key(self, payload):
        payload_str = json.dumps(payload)
        return hashlib.md5(payload_str.encode()).hexdigest()

    def get_response_fn(self, key):
        dir = "/data/perplexity"
        if not os.path.exists(dir):
            os.makedirs(dir)
        return os.path.join(dir, key + ".json")

    def load_cached_response(self, payload):
        key = self.get_payload_key(payload)
        fn = self.get_response_fn(key)
        if os.path.exists(fn):
            print("Loading cached response from " + fn)
            with open(fn, "r") as f:
                return key, json.load(f)
        return key, None

    def save_response(self, key, payload, response):
        response_cpy = {}
        response_cpy["key"] = key
        response_cpy["timestamp"] = datetime.datetime.now().isoformat()
        response_cpy["payload"] = payload
        response_cpy["response"] = response
        fn = self.get_response_fn(key)
        with open(fn, "w") as f:
            f.write(json.dumps(response_cpy, indent=4))

    def generate_completion(self, system_prompt, user_prompt):

        url = "https://api.perplexity.ai/chat/completions"

        payload = {
            "model": "sonar-pro",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            # "max_tokens": 123,
            # "temperature": 0.2,
            # "top_p": 0.9,
            # "search_domain_filter": None,
            # "return_images": False,
            # "return_related_questions": False,
            "search_recency_filter": "week",
            # "top_k": 0,
            # "stream": False,
            # "presence_penalty": 0,
            # "frequency_penalty": 1,
            # "response_format": None
        }
        headers = {
            "Authorization": "Bearer " + self.perplexity_api_key,
            "Content-Type": "application/json"
        }

        key, response = self.load_cached_response(payload)
        if response is not None:
            print(json.dumps(response, indent=4))
            return response

        print("Calling Perplexity API")
        response = requests.request("POST", url, json=payload, headers=headers)
        resp_json = response.json()
        self.save_response(key, payload, resp_json)
        print(json.dumps(resp_json, indent=4))
        key, response = self.load_cached_response(payload)
        return response
