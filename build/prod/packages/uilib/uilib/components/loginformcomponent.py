import json
from uilib.renderresponse import RenderResponse
from .verticalformcomponent import VerticalFormComponent
from uilib.components import FormTextField, FormPasswordField, FormHiddenField, FormSelectField
from ..basecomponents import Component


class LoginFormComponent(Component):

    def __init__(
        self,
        post_url,
        signup_url,
        cancel_url,
        password_reset_url,
        msg=None,
        form_attrs={},
        roles=None,
        #active_role=None,
    ):
        self.post_url = post_url
        self.signup_url = signup_url
        self.cancel_url = cancel_url
        self.password_reset_url = password_reset_url
        self.msg = msg
        self.form_attrs = form_attrs
        self.roles = roles
        # self.active_role = None

        # if self.roles is not None:
        #     default_role = list(roles.keys())[0]
        #     if active_role is None or active_role not in roles.keys():
        #         active_role = default_role

        #     self.active_role = active_role
        #     self.header_text = "%s Log In" % self.active_role.title()

        #     self.tabs = [
        #         (id, role.get("title"), role.get("url"))
        #         for id, role in self.roles.items()
        #     ]
        #     self.active_tab = self.active_role
        #     self.show_password_reset = self.roles.get(self.active_role).get(
        #         "password_reset", True
        #     )
        #     self.show_signup = self.roles.get(self.active_role).get("signup", True)
        #     self.use_username = self.roles.get(self.active_role).get(
        #         "use_username", True
        #     )
        # else:
        #     self.header_text = "Log In"
        #     self.tabs = None
        #     self.active_tab = None
        #     self.show_password_reset = True
        #     self.show_signup = True
        #     self.use_email = True
        #     self.use_username = False

        self.form_component = self._init_form_component()

    @classmethod
    def example(cls):
        return cls(
            post_url="/signin",
            signup_url="/signup",
            cancel_url="/cancel",
            password_reset_url="/password-reset",
            msg=None,
            form_attrs={},
            roles={
                "user": {"title": "User", "url": "/user"},
                "admin": {"title": "Admin", "url": "/admin"},
            }
        )

    def set_error_message(self, message):
        self.form_component.set_message(
            message, VerticalFormComponent.MESSAGE_TYPE_ERROR
        )

    def is_valid(self):
        is_valid = self.form_component.is_valid()
        if not is_valid:
            return False
        return True

    def validate(self):
        return self.form_component.validate()

    def _init_form_component(self):

        if self.msg is not None:
            msg_html = f"""
                <p style='color: red;'>
                    ERROR: {self.msg}
                </p>
            """
        else:
            msg_html = ""

        logo_src = None
        logo_alt = "Bootstrap"
        logo_width = "72"
        logo_height = "57"

        header_sub_text = msg_html
        copyright = "© 2017–2021"

        # form_css_class = ("",)
        # button_text = "Log In"
        # button_url = "/signin"

        print("LoginFormComponent Form Attrs")
        print(json.dumps(self.form_attrs, indent=4))

        show_password_reset = True
        self.show_signup = True

        if self.roles is not None:
            default_role = list(self.roles.keys())[0]

            active_role = self.form_attrs.get("role", default_role)
            if active_role is None or active_role not in self.roles.keys():
                active_role = default_role

            print("Active Role:", active_role)

            show_password_reset = self.roles.get(active_role).get(
                "password_reset", True
            )
            self.show_signup = self.roles.get(active_role).get("signup", True)

            self.use_username = self.roles.get(active_role).get(
                "use_username", True
            )

        #self.header_text = "%s Log In" % active_role.title()
        self.header_text = "Log In"

        footer_lines = []
        if show_password_reset:
            html = f"""<p class="mt-3 text-muted">Forgot password? <a href="{self.password_reset_url}" style="text-decoration: underline;">Click here</a> to reset password.</p>"""
            footer_lines.append(html)

        if self.show_signup:
            html = f"""<p class="mt-2 mb-3 text-muted">Don't have an account? <a href="{self.signup_url}" style="text-decoration: underline;">Sign Up</a></p>"""
            footer_lines.append(html)

        footer_lines.append(copyright)

        buttons = [
            ("Log In", self.post_url, "submit", True, 'md'),
            ('Cancel', self.cancel_url, "link", False, 'md'),
        ]

        component = VerticalFormComponent(
            logo_src=logo_src,
            logo_alt=logo_alt,
            logo_height=logo_height,
            header_text=self.header_text,
            header_sub_text=header_sub_text,
            form_attrs=self.form_attrs,
            footer_text_lines=footer_lines,
            post_url=self.post_url,
            buttons=buttons,
        )

        if self.roles is not None:
            role_choices = []
            for role_id, role_info in self.roles.items():
                role_choices.append((role_id, role_info.get("title"), role_info.get("url")))

            role_select_field = FormSelectField(name="role", label="Role", choices=role_choices, help="This helps us find the right account for you.")
            component.add_field(role_select_field)


        component.add_field(
            FormTextField(
                name="email_or_user", field_type="text", label="Email or Username", help=None, required=True
            )
        )
        component.add_field(
            FormPasswordField(
                name="password", label="Password", help=None, required=True
            )
        )

        # if active_role is not None:
        #     hidden_field = FormHiddenField(name="role", value=active_role)
        #     component.add_field(hidden_field)

        return component

    def render(self):
        return self.form_component.render()
