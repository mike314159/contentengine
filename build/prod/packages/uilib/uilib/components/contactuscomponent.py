from .formfields import FormTextField, FormTextAreaField, FormCaptchaField
from .verticalformcomponent import VerticalFormComponent
from ..basecomponents import Component

class ContactUsComponent(Component):

    def __init__(self, logo_src, form_attrs, post_url, cancel_url, 
        captcha_image_src, 
        error_message=None):
        self.logo_src = logo_src
        self.form_attrs = form_attrs
        self.error_message = error_message
        self.post_url = post_url
        self.cancel_url = cancel_url
        self.captcha_image_src = captcha_image_src
        self.form_component = self._get_component()


    def get_email(self):
        return self.form_component.get_field_value("email")

    def get_message(self):
        return self.form_component.get_field_value("message")

    def validate(self):
        self.form_component.validate()

    def is_valid(self, request):
        return self.form_component.is_valid()
        

    def validate_form(self, request):
        return self.form_component.validate_form(request)

    def _get_component(self):

        # logo_src = "/statics/bootstrap-logo.svg"
        logo_alt = "Logo"
        logo_height = 57

        header_text = "Contact Us"
        button_text = "Send Message"
        footer_lines = ["<br>", "<br>", "<br>", "<br>"]

        header_sub_text = ""
        footer_text_lines = footer_lines

        buttons = [
            (button_text, self.post_url, "submit", True, 'md'),
            ("Cancel", self.cancel_url, "link", False, 'md'),
        ]

        comp = VerticalFormComponent(
            logo_src=self.logo_src,
            logo_alt=logo_alt,
            logo_height=logo_height,
            header_text=header_text,
            header_sub_text=header_sub_text,
            #controls=controls,
            #button_text=button_text,
            footer_text_lines=footer_text_lines,
            #add_captcha=True,
            #captcha_image_src=self.captcha_image_src,
            #error_msg=self.error_message,
            #post_url=self.post_url,
            #cancel_url=self.cancel_url,
            form_attrs=self.form_attrs,
            buttons=buttons,
        )

        email_field = FormTextField(name="email", label="Email Address", field_type="email", required=True)    
        comp.add_field(email_field)
    
        message_field = FormTextAreaField(name="message", label="Message", required=True)
        comp.add_field(message_field)

        captcha_field = FormCaptchaField(name="captcha", label="Message", required=True, captcha_image_src=self.captcha_image_src)
        comp.add_field(captcha_field)
    
        return comp

    def render(self):
        return self.form_component.render()

    @classmethod
    def example(cls):
        return cls(
            logo_src="/statics/images/logo.png",
            form_attrs={},
            post_url="/contact",
            cancel_url="/",
            error_message=None
        )



