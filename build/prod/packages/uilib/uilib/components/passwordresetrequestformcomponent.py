from .verticalformcomponent import VerticalFormComponent
from uilib.components import FormTextField
from ..basecomponents import Component


class PasswordResetRequestFormComponent(Component):

    def __init__(self, post_url, cancel_url, form_attrs):
        self.post_url = post_url
        self.cancel_url = cancel_url
        self.form_attrs = form_attrs
        self.form_component = self._get_component()

    def get_email(self):
        email = self.form_component.get_field_value("email")
        return email.strip()

    def validate(self):
        self.form_component.validate()

    def is_valid(self, request):
        return self.form_component.is_valid()

    def set_error_msg(self, error_msg):
        self.form_component.set_message(error_msg, VerticalFormComponent.MESSAGE_TYPE_ERROR)


    def _get_component(self):

        logo_src = None
        logo_alt = "Bootstrap"
        logo_width = "72"
        logo_height = "57"

        header_sub_text = None
        copyright = "© 2017–2021"

        form_css_class = ("",)
        header_text = "Password Reset"
        header_sub_text = "Enter your email address below and we will send you a link to reset your password."
        button_text = "Send reset link"
        button_url = "/password-reset-send-email"

        password_reset_url = "/password-reset"
        signup_url = "/signup"
        footer_lines = []
        #     f'''<p class="mt-3 text-muted">Forgot password? <a href="{password_reset_url}">Click here</a> to reset password.</p>''',
        #     f'''<p class="mt-2 mb-3 text-muted">Don't have an account? <a href="{signup_url}">Sign up now</a></p>''',
        #     copyright
        # ]
        # controls = {
        #     "email": {
        #         "label": "Email Address",
        #         "type": "email",
        #     }
        # }

        buttons = [
            ("Send Reset Link", self.post_url, "submit", True, 'md'),
            ("Cancel", self.cancel_url, "link", False, 'md'),
        ]

        component = VerticalFormComponent(
            logo_src=logo_src,
            logo_alt=logo_alt,
            logo_height=logo_height,
            header_text=header_text,
            header_sub_text=header_sub_text,
            #button_text=button_text,
            footer_text_lines=footer_lines,
            buttons=buttons,
            form_attrs=self.form_attrs,
        )

        email_field = FormTextField(name="email", label="Email Address")
        component.add_field(email_field)
        return component

    def render(self):
        return self.form_component.render()
    
    @classmethod
    def example(cls):
        return cls(
            post_url="/password-reset-request",
            cancel_url="/login",
            form_attrs={}
        )


