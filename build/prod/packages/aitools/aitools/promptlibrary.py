
from openai import OpenAI
import json
import os
import sys
import time
from pydantic import BaseModel
from datetime import datetime
import hashlib
import pandas as pd
import datetime
#from tools import *
# 

class ChatPromptModel(BaseModel):
    system_prompt: str
    user_message: str
    params: dict


class PromptLibrary:

    def __init__(self, prompt_dir):
        self.prompt_dir = prompt_dir

    def get_prompt_content(self, name):
        prompt_content = open(f"{self.prompt_dir}/{name}.txt").read()
        return prompt_content


    def get_prompt(self, name):
        prompt_system = open(f"{self.prompt_dir}/{name}_system.txt").read()
        prompt_user = open(f"{self.prompt_dir}/{name}_user.txt").read()
        return prompt_system, prompt_user
    
    def get_prompt_model(self, prompt_name, params):
        prompt_system, prompt_user = self.get_prompt(prompt_name)
        return ChatPromptModel(system_prompt=prompt_system, user_message=prompt_user, params=params)
    
