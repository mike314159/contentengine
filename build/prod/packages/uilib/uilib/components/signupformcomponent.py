from .verticalformcomponent import VerticalFormComponent
from uilib.components import FormTextField, FormPasswordField, FormHiddenField
from uilib.renderresponse import RenderResponse
from ..basecomponents import Component


class SignUpFormComponent(Component):

    REQUEST_ATTR_DISCOUNT_CODE = "code"
    REQUEST_ATTR_REFERRAL_SOURCE = "source"
    PASSWORD_MIN_LENGTH = 8

    def __init__(self, post_url, sign_in_url, cancel_url, msg=None, view='default', form_attrs={}):
        self.post_url = post_url
        self.sign_in_url = sign_in_url
        self.cancel_url = cancel_url
        self.msg = msg
        self.form_attrs = form_attrs
        self.password_confirm = False

        if view == 'default':
            self.settings = {
                'title': 'Sign Up',
                'fields': ['first_name', 'email', 'password'],
                'buttons': [
                    ("Sign Up", self.post_url, "submit", True, None),
                    ("Cancel", self.cancel_url, "link", False, None),
                ],
                'show_sign_in_link': True,
            }

        if view == 'basic':
            self.settings = {
                'title': 'Free Math Assessment',
                'fields': ['email'],
                'buttons': [
                    ("Get Started", self.post_url, "submit", True, "large"),
                    #("Cancel", self.cancel_url, "link", False),
                ],
                'show_sign_in_link': False,
            }


        self.form_component = self._init_form_component()


    def set_error_message(self, message):
        self.form_component.set_message(
            message, VerticalFormComponent.MESSAGE_TYPE_ERROR
        )

    def _init_form_component(self):

        if self.msg is not None:
            msg_html = f"""
                <p style='color: red;'>
                    ERROR: {self.msg}
                </p>
            """
        else:
            msg_html = "Enter your information below and we will email you a verification link to get started."

        logo_src = None
        logo_alt = "Bootstrap"
        logo_height = "57"

        header_text = self.settings.get('title', 'Sign Up')
        header_sub_text = msg_html

        # buttons = [
        #     ("Sign Up", self.post_url, "submit", True),
        #     ("Cancel", self.cancel_url, "link", False),
        # ]
        buttons = self.settings.get('buttons', [])

        show_sign_in_link = self.settings.get('show_sign_in_link', True)
        if show_sign_in_link:
            footer_lines = [
                f"""Already have an account? <a href='{self.sign_in_url}' style='color: blue; text-decoration: underline;'>Sign In</a>"""
            ]
        else:
            footer_lines = []


        discount_code_hidden_field = FormHiddenField(name=self.REQUEST_ATTR_DISCOUNT_CODE)
        referral_source_hidden_field = FormHiddenField(name=self.REQUEST_ATTR_REFERRAL_SOURCE)

        component = VerticalFormComponent(
            css_id='signup-form',
            logo_src=logo_src,
            logo_alt=logo_alt,
            logo_height=logo_height,
            header_text=header_text,
            header_sub_text=header_sub_text,
            # button_text=button_text,
            footer_text_lines=footer_lines,
            # post_url=self.post_url,
            form_attrs=self.form_attrs,
            # cancel_url=self.cancel_url,
            # cancel_text="Cancel",
            buttons=buttons,
        )

        fields = self.settings.get('fields', [])
        for field_name in fields:
            if field_name == 'first_name':
                name_field = FormTextField(name="name", label="First Name", required=True, help="We use this to personalize your experience.")
                component.add_field(name_field)
            if field_name == 'email':
                email_field = FormTextField(name="email", label="Email Address", required=True)
                component.add_field(email_field)
            if field_name == 'password':
                password_field = FormPasswordField(
                    name="password", label="Password", required=True
                )
                component.add_field(password_field)
            if field_name == 'password_confirm':
                password_confirm_field = FormPasswordField(
                    name="password_confirm", label="Password Confirmation", required=True,
                    help=f"Minimum {self.PASSWORD_MIN_LENGTH} characters."
                )
                component.add_field(password_confirm_field)

        return component

    def is_valid(self):
        is_valid = self.form_component.is_valid()
        if not is_valid:
            return False

        password_field = self.form_component.get_field("password")
        print("Password field: ", password_field)
        if password_field is not None:
            if len(password_field.value) < self.PASSWORD_MIN_LENGTH:
                password_field.set_error(f"Password must be at least {self.PASSWORD_MIN_LENGTH} characters")
                return False

            if self.password_confirm:
                password_confirm_field = self.form_component.get_field("password_confirm")
                if password_field.value == password_confirm_field.value:
                    return True
                else:
                    password_field.set_error("Passwords do not match")
                    password_confirm_field.set_error("Passwords do not match")
                    return False

        return True

    def validate(self):
        return self.form_component.validate()

    def render(self):
        if self.form_component is not None:
            return self.form_component.render()
        return RenderResponse(html="")

    @classmethod
    def example(cls):
        return cls(
            post_url="/signup", 
            sign_in_url="/signin",
            cancel_url="/", 
            msg=None, 
            form_attrs={}
        )
