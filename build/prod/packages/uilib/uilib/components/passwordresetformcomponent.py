from .verticalformcomponent import VerticalFormComponent
from uilib.components import FormTextField, FormPasswordField, FormHiddenField
from ..basecomponents import Component


class PasswordResetFormComponent(Component):

    def __init__(self, post_url, cancel_url, form_attrs):
        self.post_url = post_url
        self.cancel_url = cancel_url
        self.form_attrs = form_attrs
        self.form_component = self._get_component()

    # def get_email(self):
    #     email = self.form_component.get_field_value("email")
    #     return email.strip()

    def validate(self):
        self.form_component.validate()

    def is_valid(self, request):

        if not self.form_component.is_valid():
            return False
        
        password_field  = self.form_component.get_field("password")
        password_confirm_field = self.form_component.get_field("password_confirm")

        if password_field.value == password_confirm_field.value:
            return True
        else:
            password_field.set_error("Passwords do not match")
            password_confirm_field.set_error("Passwords do not match")
            return False
            
    def get_user_guid(self):
        hidden_guid_field = self.form_component.get_field("guid")
        return hidden_guid_field.value

    def get_password(self):
        password_field  = self.form_component.get_field("password")
        return password_field.value 

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
        header_sub_text = "Enter and confirm your new password."
        #button_text = "Change Password"
        #button_url = "/password-reset-send-email"

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
            ("Change Password", self.post_url, "submit", True, 'md'),
            ("Cancel", self.cancel_url, "link", False, 'md'),
        ]

        component = VerticalFormComponent(
            logo_src=logo_src,
            logo_alt=logo_alt,
            logo_height=logo_height,
            header_text=header_text,
            header_sub_text=header_sub_text,
            footer_text_lines=footer_lines,
            buttons=buttons,
            form_attrs=self.form_attrs,
        )

        fields_disabled = False
        # email_field = FormTextField(name="email", label="Email Address")
        # component.add_field(email_field)

        password_field = FormPasswordField(name="password", label="Password", help='', required=True, disabled=fields_disabled)
        component.add_field(password_field)

        confirm_password_field = FormPasswordField(name="password_confirm", label="Password Confirmation", help='', 
                                                   required=True, disabled=fields_disabled)
        component.add_field(confirm_password_field)

        hidden_guid_field = FormHiddenField(name="guid")
        component.add_field(hidden_guid_field)

        hidden_token_field = FormHiddenField(name="token")
        component.add_field(hidden_token_field)

        return component

    def render(self):
        return self.form_component.render()
    
    @classmethod
    def example(cls):
        return cls(
            post_url="/password-reset",
            cancel_url="/login",
            form_attrs={}
        )


