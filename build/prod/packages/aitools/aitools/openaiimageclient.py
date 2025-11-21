



from openai import OpenAI
import base64
import os
import hashlib


class OpenAIImageClient:


    def __init__(self, openai_api_key, cache_dir=None):

        self.client = OpenAI(
            api_key=openai_api_key, 
        )
        self.cache_dir = cache_dir
        if cache_dir is not None:
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
            self.cache_dir = cache_dir


    def generate(self, prompt, override_cache_dir=None):

        if override_cache_dir is not None:
            cache_dir = override_cache_dir
        else:
            cache_dir = self.cache_dir

        key = hashlib.md5(prompt.encode()).hexdigest()
        fn = f"{key}.png"
        ffn = os.path.join(cache_dir, fn)
        if os.path.exists(ffn):
            return ffn

        # response = self.client.responses.create(
        #     model="gpt-image-1",
        #     input=prompt,
        #     tools=[{"type": "image_generation"}],
        # )

        result = self.client.images.generate(
            model="gpt-image-1",
            prompt=prompt
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)


        # # Save the image to a file
        # image_data = [
        #     output.result
        #     for output in response.output
        #     if output.type == "image_generation_call"
        # ]
            
        with open(ffn, "wb") as f:
            f.write(image_bytes)

        return ffn


# def main():
#     client = OpenAI() 
#     response = client.responses.create(
#         model="gpt-5",
#         input="Generate an image of gray tabby cat hugging an otter with an orange scarf",
#         tools=[{"type": "image_generation"}],
#     )
#     save_image(response)

#     image_data = [
#         output.result
#         for output in response.output
#         if output.type == "image_generation_call"
#     ]
#     if image_data:
#         image_base64 = image_data[0]
#         with open("otter.png", "wb") as f:
#             f.write(base64.b64decode(image_base64))


# if __name__ == "__main__":
#     main()