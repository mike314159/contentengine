from ..renderresponse import RenderResponse
from ..basecomponents import Component


class NewsletterSignupVerticalFormComponent(Component):

    def __init__(self, logo_src, form_attrs, error_message=None):
        self.logo_src = logo_src
        self.form_attrs = form_attrs
        self.error_message = error_message
        # self.captcha_image_src = captcha_image_src

    def render(self):

        header_text = "Newsletter Signup"
        header_sub_text = NewsletterSignupComponent.PITCH_TEXT
        button_text = "Subscribe Now"

        comp = VerticalFormComponent(
            logo_src=self.logo_src,
            header_text=header_text,
            header_sub_text=header_sub_text,
            button_text=button_text,
        )
        comp.add_email_field(id="email", label="Email Adress")
        return comp.render()

    @staticmethod
    def example():
        pass