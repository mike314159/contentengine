

import os
import random
import json
import sys
import re
import time
import datetime
from openai import OpenAI
#from utils.secrets_store import get_secret

class ChatMessage:

    def __init__(self, role, content):
        self.role = role
        self.content = content


class OpenAIChatClient:

    RESPONSE_TYPE_LIST = "list"
    RESPONSE_TYPE_DICT = "dict"
    RESPONSE_TYPE_STR = "str"

    def __init__(self, openai_api_key, model = "gpt-4o"):
        # self.api_key = api_key
        # self.api_version = "2020-05-20"
        # self.api_url = "https://api.openai.com"
        self.model = model


        self.client = OpenAI(
            #temperature=temperature, 
            api_key=openai_api_key, 
            #model_name=model_name
        )
    


    def complete(self, messages, tools=[]):

        # Step 1: send the conversation and available functions to the model
        # OpenAI API is expecting messages to resemble the following:
        # messages = [
        #     {
        #         "role": "user",
        #         "content": "Why is the sky blue?",
        #     }
        # ]

        msgs = []
        for message in messages:
            d = {
                "role": message.role,
                "content": message.content,
            }
            msgs.append(d)

        '''
        To force the model to always call one or more functions, you can set tool_choice: "required". The model will then select which function(s) to call.
        To force the model to call only one specific function, you can set tool_choice: {"type": "function", "function": {"name": "my_function"}}.
        To disable function calling and force the model to only generate a user-facing message, you can set tool_choice: "none".
        '''
        # tools = [
        #     {
        #         "type": "function",
        #         "function": {
        #             "name": "get_current_weather",
        #             "description": "Get the current weather in a given location",
        #             "parameters": {
        #                 "type": "object",
        #                 "properties": {
        #                     "location": {
        #                         "type": "string",
        #                         "description": "The city and state, e.g. San Francisco, CA",
        #                     },
        #                     "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        #                 },
        #                 "required": ["location"],
        #             },
        #         },
        #     }
        # ]
        #tools = []

        if tools is not None and len(tools) > 0:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=msgs,
                tools=tools,
                tool_choice="auto"
            )
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=msgs
            )
        #print("Response\n", response)
        #sys.exit()

        '''
        Response
            ChatCompletion(
                id='chatcmpl-8SWp4yc9tYcgKOhdbq9SqIYohEJR0', 
                choices=[Choice(finish_reason='tool_calls', 
                index=0, 
                message=ChatCompletionMessage(
                    content=None, 
                    role='assistant', 
                    function_call=None, 
                    tool_calls=[
                        ChatCompletionMessageToolCall(
                            id='call_qf9kpCWAwcA2HY8ipzM6H7Pj', 
                            function=Function(arguments='{"location": "San Francisco", "unit": "celsius"}', 
                            name='get_current_weather'), type='function'), 
                        ChatCompletionMessageToolCall(
                            id='call_lxUCPTOq3yy92QhlmGnd8xSO', 
                            function=Function(arguments='{"location": "Tokyo", "unit": "celsius"}', 
                            name='get_current_weather'), type='function'), 
                        ChatCompletionMessageToolCall(id='call_615pGXQReLTxc4TAEBb3K3z5', 
                        function=Function(arguments='{"location": "Paris", "unit": "celsius"}', 
                        name='get_current_weather'), type='function')]))
                    ], 
                    created=1701810046, 
                    model='gpt-3.5-turbo-1106', 
                    object='chat.completion', 
                    system_fingerprint='fp_eeff13170a', 
                    usage=CompletionUsage(completion_tokens=77, prompt_tokens=88, total_tokens=165))

        '''

        response_message = response.choices[0].message
        response_content = response_message.content
        tool_calls = response_message.tool_calls

        # https://platform.openai.com/docs/guides/function-calling
        function_calls = []
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                #function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)     
                function_calls.append((function_name, function_args))

        return response_content, function_calls
    
        # # Step 2: check if the model wanted to call a function
        # if tool_calls:

        #     # Step 3: call the function
        #     # Note: the JSON response may not always be valid; be sure to handle errors
        #     available_functions = {
        #         "get_current_weather": get_current_weather,
        #     }  # only one function in this example, but you can have multiple
        #     messages.append(response_message)  # extend conversation with assistant's reply
        #     # Step 4: send the info for each function call and function response to the model
        #     for tool_call in tool_calls:

        #         function_name = tool_call.function.name
        #         function_to_call = available_functions[function_name]
        #         function_args = json.loads(tool_call.function.arguments)

        #         function_response = function_to_call(
        #             location=function_args.get("location"),
        #             unit=function_args.get("unit"),
        #         )

        #         messages.append(
        #             {
        #                 "tool_call_id": tool_call.id,
        #                 "role": "tool",
        #                 "name": function_name,
        #                 "content": function_response,
        #             }
        #         )  
            
        #     # extend conversation with function response
        #     second_response = self.client.chat.completions.create(
        #         model="gpt-3.5-turbo-1106",
        #         messages=messages,
        #     )  # get a new response from the model where it can see the function response
        #     return second_response


    def _strip_invalid_json_chars(json_string):
        # Use regular expressions to find the first and last valid JSON characters
        match = re.search(r'[\[{]', json_string)
        if match:
            start = match.start()
            #print("Start: %d" % start)
        else:
            return None  # No valid JSON structure found
        
        match = re.search(r'[\]}]', json_string[::-1])
        if match:
            end = len(json_string) - match.start()
            #print("End: %d" % end)
        else:
            return None  # No valid JSON structure found
        
        # Return the cleaned JSON string
        return json_string[start:end]
    

    def _load_json(self, json_string):
        json_string = OpenAIChatClient._strip_invalid_json_chars(json_string)
        print("Loading Json String\n%s" % json_string)
        if json_string is None:
            return None
        try:
            obj = json.loads(json_string)
            print("Loaded Json Object Type: %s\n%s" % (type(obj), obj))
            return obj
        except:
            print("Error parsing response json")
            print("%s" % json_string)
            return None

    # This is a simpler API for the caller.
    def generate(self, prompt, expected_response_type, sleep_time=None):

        assert expected_response_type in [OpenAIChatClient.RESPONSE_TYPE_LIST, 
                                          OpenAIChatClient.RESPONSE_TYPE_DICT, 
                                          OpenAIChatClient.RESPONSE_TYPE_STR]
        assert prompt is not None
        assert prompt != ""

        settings = {
            "model": self.model,
            "response_type": expected_response_type,
            "timestamp": datetime.datetime.now().isoformat()
        }

        messages = [
            ChatMessage(role="system", content=prompt),
        ]
        #print("Prompt\n", prompt)
        #print("Messages\n", messages)

        response_message, tool_calls = self.complete(messages)
        #print("Open AI response")
        #print("Message Type: %s" % type(response_message))
        #print("Message\n", response_message)

        if expected_response_type == OpenAIChatClient.RESPONSE_TYPE_STR:
            response = response_message
        elif expected_response_type == OpenAIChatClient.RESPONSE_TYPE_LIST:
            response = self._load_json(response_message)
        elif expected_response_type == OpenAIChatClient.RESPONSE_TYPE_DICT:
            response = self._load_json(response_message)
        else:
            assert False, "Invalid expected response type: %s" % expected_response_type


        #print("Response: ", response)

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

        # if response is not None:
        #     if response_format == 'html':
        #         self._save_text_to_file(response_fn, response)
        #     elif response_format == 'json':
        #         self._save_json_to_file(response_fn, response)
        #     else:
        #         assert False, "Invalid response format: %s" % response_format
        #     self._save_text_to_file(prompt_fn, prompt)  # Save prompt
        #     self._save_json_to_file(settings_fn, settings)  # Save settings

        # if sleep_time is None:
        #     sleep_time = random.randint(10, 60)
        # print("Sleeping for %d seconds" % sleep_time)
        if sleep_time is not None:
            time.sleep(sleep_time)
        return (settings, response)


    def generate_json(self, system_prompt, user_message, model_class, sleep_time=None):

        # model_obj is a pydantic model similr to this example:
        # class CalendarEvent(BaseModel):
        #     name: str
        #     date: str
        #     participants: list[str]

        settings = {
            "model": self.model,
            "response_type": "json",
            "timestamp": datetime.datetime.now().isoformat()
        }

        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            response_format=model_class,
        )

        response = completion.choices[0].message.parsed
        return (settings, response)


    def generate_text(self, system_prompt, user_message):

        settings = {
            "model": self.model,
            "response_type": "text",
            "timestamp": datetime.datetime.now().isoformat()
        }

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ]
        )

        response = completion.choices[0].message.content
        return (settings, response)




    def generate_model(self, system_prompt, user_message, model_class, sleep_time=None):

        settings = {
            "model": self.model,
            "response_type": "model",
            "model_class": model_class.__name__,
            "timestamp": datetime.datetime.now().isoformat()
        }

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
            return (settings, response)
        except Exception as e:
            print("Error generating model: %s" % e)
            return None, None
    

