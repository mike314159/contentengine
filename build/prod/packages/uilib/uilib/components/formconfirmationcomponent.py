from uilib.renderresponse import RenderResponse
from ..basecomponents import Component

class FormConfirmationComponent(Component):

    def __init__(
        self,
        logo_src=None,
        logo_alt=None,
        header_text="Title",
        header_sub_text="Subtitle",
        button_text=None,
        button_url="",
        redirect_url="",
        buttons=None,
    ):
        self.logo_src = logo_src
        self.logo_alt = logo_alt
        self.header_text = header_text
        self.header_sub_text = header_sub_text
        #self.button_text = button_text
        #self.button_url = button_url
        self.logo_width = "72"
        self.redirect_url = redirect_url
        self.buttons = buttons

    def _render_buttons(buttons):
        if buttons is None:
            return ""
        buttons_html = ""
        for button in buttons:
                active = button.get('active', True)
                active_css = "active" if active else ""
                buttons_html += f"""
                <a href="{button.get('url', '')}" class="w-40 btn btn-md btn-primary {active_css}">{button.get('text', '')}</a>
            """
        buttons_html += ""
        return buttons_html
    
    def render(self):

        if self.header_sub_text is None:
            header_sub_text_html = ""
        else:
            header_sub_text_html = (
                f"""<p class="mt-4 mb-3 form-description">{self.header_sub_text}</p>"""
            )

        if self.logo_src is None:
            logo_html = ""
        else:
            logo_html = f"""
                <img class="mb-4" src="{self.logo_src}" alt="{self.logo_alt}" width="{self.logo_width}">
            """
        redirect_script = ""
        if self.redirect_url:
            redirect_script = f"""
            <script>
                setTimeout(function() {{
                    window.location.href = "{self.redirect_url}";
                }}, 5000);
            </script>
            """

        buttons_html = ""
        if self.buttons is not None:
            buttons_html = "<div>"
            buttons_html += FormConfirmationComponent._render_buttons(self.buttons)
            buttons_html += "</div>"
        # else:
        #     buttons_html = f"""
        #         <a href="{self.button_url}" class="w-40 btn btn-md btn-primary">{self.button_text}</a>
        #     """

        html = f"""
          <div style="text-align: center;  margin-left: auto; margin-right: auto; margin-top: 70px; margin-bottom: 40px; min-width: 400px; width: 50%; ">
            {logo_html}
            <h1>{self.header_text}</h1>
            {header_sub_text_html}
            <br>
            {buttons_html}
          </div>
          {redirect_script}
        """
        return RenderResponse(html=html)

    @classmethod
    def example(cls, view="signup_success"):
        site_name = "Example Site"
        logo_src = "/statics/logo.png"
        logo_height = 40
        home_page_url = "/"
        header_text = "Title"
        header_sub_text = "Subtitle"
        button_text = "Button"
        button_url = "/"
        logo_alt = "Logo"

        if view == 'signup_success':
            comp = cls(
                header_text="Sign Up Successful",
                header_sub_text="Check your email for an account verification link.",
                button_text="Return to Home",
                button_url=button_url,
            )
        elif view == 'signup_failure':
            comp = cls(
                header_text="Sign Up Failed",
                header_sub_text="Please try again.",
                button_text="Return to Home",
                button_url=button_url,
            )
        else:
            comp = cls(
                header_text="Form Submitted",
                header_sub_text="Thank you for your submission.",
                button_text="Continue",
                button_url=button_url,
            )
        return comp
    
