
from uilib.basecomponents import Component
from uilib.renderresponse import RenderResponse
from uilib.components import *
from .formfields import FormTextField, FormPasswordField, FormHiddenField, FormSelectField


class VerticalFormComponent(Component):

    MESSAGE_TYPE_SUCCESS = "success"
    MESSAGE_TYPE_ERROR = "error"

    def __init__(
        self,
        logo_src=None,
        logo_alt=None,
        logo_height=72,
        header_text=None,
        header_sub_text=None,
        #controls=None,
        button_text="Submit",
        footer_text_lines=[],
        #add_captcha=False,
        #captcha_image_src=None,
        form_attrs={},
        css_id=None,
        tabs=None,
        active_tab=None,
        align_center=True,
        post_url=None,
        cancel_url=None,
        cancel_text="Cancel",
        confirm_url=None,
        buttons = [],
    ):
        self.id = id
        self.logo_src = logo_src
        self.logo_alt = logo_alt
        self.logo_height = logo_height
        self.header_text = header_text
        self.header_sub_text = header_sub_text
        self.button_text = button_text
        self.footer_text_lines = footer_text_lines
        #self.error_msg = None
        #self.add_captcha = add_captcha
        #self.captcha_image_src = captcha_image_src
        self.align_center = align_center
        self.form_attrs = form_attrs
        self.tabs = tabs
        self.active_tab = active_tab
        #if controls is None:
        self.controls = []
        #   else:
        #       self.controls = controls
        #self.controls_order = []
        self.css_id = css_id
        self.post_url = post_url
        self.cancel_url = cancel_url
        self.cancel_text = cancel_text
        self.message = None
        self.message_type = None
        self.confirm_url = confirm_url
        self.confirm_text = "OK"
        self.buttons = buttons


    #def set_error_msg(self, error_msg):
    #    self.error_msg = error_msg

    def set_message(self, message, message_type):
        self.message = message
        self.message_type = message_type

    def set_error_message(self, message):
        self.set_message(
            message, VerticalFormComponent.MESSAGE_TYPE_ERROR
        )

    def get_field(self, id):
        for control in self.controls:
            if control.name == id:
                return control
        return None




    def validate(self):
        for control in self.controls:
            control.validate()

    def is_valid(self):
        for control in self.controls:
            if not control.is_valid():
                return False
        return True

    def validate_form(self, request):
        is_valid = True
        for control in self.controls:
            field_is_valid = control.validate_field(request)
            if not field_is_valid:
                is_valid = False
        return is_valid
    
    def get_field_value(self, field_name):
        field = self.get_field(field_name)
        if field is not None:
            return field.value
        else:
            return None

    def _get_value(self, id, default_value=None):
        #print("Get value for ", id)
        #print("Form attrs: ", json.dumps(self.form_attrs, indent=4))
        form_value = self.form_attrs.get(id, None)
        #print("Got value: ", form_value)
        if form_value is not None:
            value = form_value
        else:
            if default_value is None:
                value = ""
            else:
                value = default_value
        return value

    # def add_input_field(self, id, label, placeholder="", help_text=None, value=None):
    #     self.controls[id] = {
    #             "id": id,
    #             "label": label,
    #             "placeholder": placeholder,
    #             "help_text": help_text,
    #             "type": "text",
    #             "value": self._get_value(id, value),
    #         }
    #     self.controls_order.append(id)

    # def add_text_field(self, id, label, placeholder="", help_text=None, value=None):
    #     self.add_input_field(id, label, placeholder, help_text, value)

    # def add_email_field(self, id, label, placeholder="", help_text=None, value=None):
    #     self.controls[id] = {
    #             "id": id,
    #             "label": label,
    #             "placeholder": placeholder,
    #             "help_text": help_text,
    #             "type": "email",
    #             "value": self._get_value(id, value),
    #         }
    #     self.controls_order.append(id)


    # def add_password_field(self, id, label, placeholder="", help_text=None, value=None):
    #     self.controls[id] = {
    #             "id": id,
    #             "label": label,
    #             "placeholder": placeholder,
    #             "help_text": help_text,
    #             "type": "password",
    #             "value": self._get_value(id, value),
    #         }
    #     self.controls_order.append(id)

    def add_field(self, field):
        value = self._get_value(field.name, None)
        field._set_value(value)
        #print("Adding field: ", field.name, " value: ", value)
        self.controls.append(field)
        #self.controls_order.append(field.name)


    def _get_html(self, value, html):
        if value is not None:
            return html
        else:
            return ""

    def _field_help_tmpl(self, help_text, help_block_id):
        if help_text is None:
            return ""
        else:
            return f"""
                        <div id="{help_block_id}" class="form-text mb-1 mt-0">
                        {help_text}
                        </div>
                    """
        
    def _field_tmpl(self, field_html, help_text):
        help_block = self._field_help_tmpl(help_text, help_block_id)
        html = f"""
            <div class="mb-4">
                <label for="{id}" class="form-label fw-semibold mb-1" style="display: inline-block; text-align: left !important; width: auto;">{label}</label>
                {help_block}
                {field_html}
            </div>
        """
        return html
    
    def disable_fields(self):
        for control in self.controls:
            control.disable()

    def render(self):

        if self.message is not None:
            if self.message_type == self.MESSAGE_TYPE_SUCCESS:
                alert_class = "alert-success"
            elif self.message_type == self.MESSAGE_TYPE_ERROR:
                alert_class = "alert-danger"
            else:
                alert_class = ""

            message_html = f"""
            <div class="alert {alert_class}" role="alert">
                {self.message}
            </div>
            """
        else:
            message_html = ""

        controls_html = []
        controls_js = []
        hidden_fields = []
        for control in self.controls:
            control_html, control_js = control.render()
            controls_html.append(control_html)
            controls_js.append(control_js)

        controls_html = "\n".join(controls_html)
        controls_js = "\n".join(controls_js)
        footer = []
        for line in self.footer_text_lines:
            footer.append(f'<p class="mt-2 mb-3 text-muted">{line}</p>')
        footer_html = "\n".join(footer)

        if self.header_sub_text is None:
            header_sub_text_html = ""
        else:
            header_sub_text_html = (
                f"""<p class="mt-2 mb-3 form-description">{self.header_sub_text}</p>"""
            )

        # if self.captcha_image_src is not None:
        #     print("Captcha image src:", self.captcha_image_src)
        #     captcha_html = f"""
        #     <div class="mb-3">
        #         <img src='{self.captcha_image_src}' alt='captcha' style='height: 100px;' />
        #     </div>
        #     """
        #     captcha_field = FormTextField(name="captcha", label="Captcha")
        #     captch_input_html, captch_input_js = captcha_field.render()
        #     captcha_html += captch_input_html
        # else:
        captcha_html = ""

        logo_html = self._get_html(
            self.logo_src,
            f"""<img class="mb-4" src="{self.logo_src}" alt="{self.logo_alt}" height="{self.logo_height}">""",
        )

        if self.align_center:
            align_style = "text-align: center;"
        else:
            align_style = "text-align: left;"

        heading_html = self._get_html(
            self.header_text,
            # f'''<h1 class="h3 mb-3 fw-normal">{self.header_text}</h1>'''
            f"""<h1 style="{align_style}">{self.header_text}</h1>""",
        )
        css_id = self._get_html(self.css_id, f'id="{self.css_id}"')

        tab_items_html = ""
        if self.tabs is not None:
            for id, label, url in self.tabs:
                if id == self.active_tab:
                    active_class = "active"
                    style = "background-color: rgb(234, 234, 255); text-decoration-color: black;"
                else:
                    active_class = ""
                    style = "background-color: white; border-width: 1px; border-color: lightgray; color: black;"
                tab_items_html += f"""
                <li class="nav-item">
                    <a class="nav-link {active_class}" href="{url}" style="{style}">{label}</a>
                </li>
                """

        if tab_items_html == "":
            tabs_html = ""
        else:
            tabs_html = f"""
            <ul class="nav nav-tabs justify-content-end mb-5" style="nav-pills-link-active-color: red;">
                {tab_items_html}
            </ul>
            """

        #          <div style="text-align: center;  margin-left: auto; margin-right: auto; margin-top: 70px; margin-bottom: 40px; min-width: 400px; width: 50%; ">

        header = f"""
          <div style="text-align: center; margin-bottom: 40px;">
            {logo_html}
            {tabs_html}
            {heading_html}
            {header_sub_text_html}
          </div>
        """

        hidden_fields_html = "\n".join(hidden_fields)

        # if self.align_center:
        #     align_style = "margin: auto;"
        # else:
        #     align_style = "margin-left: 0; padding-left: 0; margin-right: auto;"


        buttons = []

        # if self.buttons is None:
        #     if self.post_url is not None:
        #         buttons.append(f"""<button class="btn btn-md btn-primary" type="submit">{self.button_text}</button>""")
        #     if self.confirm_url is not None:
        #         buttons.append(f"""<a href="{self.confirm_url}" class="btn btn-md btn-primary">{self.confirm_text}</a>""")
        #     if self.cancel_url is not None:
        #         buttons.append(f"""<a href="{self.cancel_url}" class="btn btn-md btn-secondary">{self.cancel_text}</a>""")
        # else:

        for (text, url, button_type, active, size) in self.buttons:
            if active:
                active_class = "active"
            else:
                active_class = ""
            if size == "large":    
                size_class = "btn-lg"
            else:
                size_class = "btn-md"

            if button_type == "submit":
                buttons.append(f"""<button class="btn {size_class} btn-primary {active_class}" type="submit">{text}</button>""")
                self.post_url = url
            elif button_type == "link":
                buttons.append(f"""<a href="{url}" class="btn {size_class} btn-primary {active_class}">{text}</a>""")

        buttons_html = "&nbsp;&nbsp;".join(buttons)

        #container_style = f"""style='text-align: left; min-width: 400px; width: 50%; {align_style}'"""
        #            <div {css_id} {container_style} class="container">
        html = f"""
            {header}
            <form id="form" style='margin-top: 20px;'" method="post" action={self.post_url}>
                {message_html}
                {controls_html}
                {hidden_fields_html}
                {captcha_html}
                <div style="{align_style} margin-top: 40px;">
                    {buttons_html}
                </div>
                <div style="text-align: center; margin-top: 30px;">
                    {footer_html}
                </div>
            </form>
        """
        #           </div>
        javascript = ""
        return RenderResponse(html=html, footer_js=controls_js)

    @classmethod
    def example(cls, view="signup"):
        logo_src = None
        logo_alt = "Bootstrap"
        logo_width = "72"
        logo_height = "57"

        copyright = "© 2017–2021"

        header_sub_text = None

        fields = []

        if view == "signup":
            form_css_class = ("signup-form",)
            header_text = "Sign Up"
            button_text = "Sign Up"
            button_url = "/signup"

            footer_lines = [
                f"Already have an account? <a href='/signin'>Sign In</a>",
                copyright,
            ]
            # controls = {
            #     "email": {
            #         "label": "Email Address",
            #         "type": "email",
            #     },
            #     "password": {
            #         "label": "Password",
            #         "type": "password",
            #     },
            #     "password_confirm": {
            #         "label": "Password Confirmation",
            #         "type": "password",
            #     },
            # }
            fields = [
                FormTextField("email", "Email Address", "Enter your email address"),
                FormTextField("password", "Password", "Enter your password"),
                FormTextField("password_confirm", "Password Confirmation", "Enter your password again"),
            ]

        if view == "signin":
            form_css_class = ("",)
            header_text = "Log In"
            button_text = "Log In"
            button_url = "/signin"

            password_reset_url = "/password-reset"
            signup_url = "/signup"
            footer_lines = [
                f"""<p class="mt-3 text-muted">Forgot password? <a href="{password_reset_url}" style="text-decoration: underline;">Click here</a> to reset password.</p>""",
                f"""<p class="mt-2 mb-3 text-muted">Don't have an account? <a href="{signup_url}" style="color: #000000;">Sign up now</a></p>""",
                copyright,
            ]
            # controls = {
            #     "email": {
            #         "label": "Email Address",
            #         "type": "email",
            #     },
            #     "password": {
            #         "label": "Password",
            #         "type": "password",
            #     },
            # }
            fields = [
                FormTextField("email", "Email Address", "Enter your email address"),
                FormTextField("password", "Password", "Enter your password"),
            ]

        if view == "password-reset":
            form_css_class = ("",)
            header_text = "Reset Your Password"
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
            controls = {
                "email": {
                    "label": "Email Address",
                    "type": "email",
                }
            }
            fields = [
                FormTextField("email", "Email Address", "Enter your email address"),
            ]

        component = cls(
            logo_src=logo_src,
            logo_alt=logo_alt,
            logo_height=logo_height,
            header_text=header_text,
            header_sub_text=header_sub_text,
            #controls=controls,
            button_text=button_text,
            footer_text_lines=footer_lines,
        )

        for field in fields:
            component.add_field(field)
        return component
