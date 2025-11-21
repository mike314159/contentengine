

import hashlib
import random
from captcha.image import ImageCaptcha
from uilib.basecomponents import Component


class Captcha:

    def __init__(self):
        self.image = ImageCaptcha(width=200, height=100)
        pass

    def generate(self, code):
        return self.image.generate(code)
    

    def get_captcha_choices(self, request):
        ip_addr = request.remote_addr
        ip_addr = ip_addr.replace(".", "")
        str_2_hash = "prefix_" + ip_addr
        result = hashlib.md5(str_2_hash.encode()).hexdigest().upper()
        return result


    def get_random_captcha_image(self, request):
        choices = self.get_captcha_choices(request)
        start_idx = random.randint(0, len(choices) - 5)
        code = choices[start_idx : start_idx + 4]
        data = self.image.generate(code)
        return data


    def is_valid_captcha(self, request, code):
        if code is None:
            return False
        if len(code) != 4:
            return False
        choices = self.get_captcha_choices(request)
        #print("Choices:", choices)
        return code in choices

    # def get_captcha_image(request):
    #     image = ImageCaptcha(width=200, height=100)
    #     return image


