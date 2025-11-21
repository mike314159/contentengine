from ..renderresponse import RenderResponse
from ..basecomponents import Component


class NewsletterSignupComponent(Component):

    PITCH_TEXT = """Get information on new features, updates, and more. We respect your privacy. And we will never spam you. Unsubscribe at any time."""

    def __init__(self, post_url):
        # self.logo_src = logo_src
        # self.form_attrs = form_attrs
        # self.error_message = error_message
        # self.captcha_image_src = captcha_image_src
        self.post_url = post_url

    def get_input_group_html(post_url, error_msg=None):

        hx_target = "newsletter-email-div"

        htmx = f"""
            hx-post="{post_url}" hx-trigger="click" hx-target="#{hx_target}" hx-swap="outerHTML"
        """

        if error_msg is not None:
            error_html = f"""
                <p style='color: red;'>
                    {error_msg}
                </p>
            """
        else:
            error_html = ""

        html = f"""
            <div id="{hx_target}">
                <form method="post">
                    <div class="input-group">
                        <input id='email' name='email' type="email" class="form-control" placeholder="Enter your email" style='margin-right: 10px;'>
                        <span class="input-group-btn">
                            <button class="btn" {htmx} style='color: #fff; background: #243c4f;'>Subscribe Now</button>
                        </span>
                    </div>
                </form>
                {error_html}
            </div>
        """
        return html

    def render(self):

        input_group_html = NewsletterSignupComponent.get_input_group_html(
            self.post_url, None
        )

        html = f"""
        <section class="newsletter" style='padding: 80px 0; background: #d5e1df;'>
            <div class="container">
                <div class="row">
                    <div class="col-sm-12">
                        <div class="content">
                            <h2 style='color: dark-grey;'>Subscribe to our Newsletter</h2>
                            <p class="form-text">{NewsletterSignupComponent.PITCH_TEXT}</div>
                            
                                {input_group_html}
                            
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """
        return RenderResponse(html=html)

        header_text = "Newsletter Signup"
        button_text = "Signup"

        footer_lines = []
        controls = [
            {
                "id": "email",
                "label": "Email Address",
                "type": "email",
                "value": self.form_attrs.get("email", ""),
            }
        ]

        header_sub_text = "Subscribe to our newsletter. Get information on new features, updates, and more. We respect your privacy. And we will never spam you. Unsubscribe at any time."
        footer_text_lines = footer_lines

        logo_src = None
        logo_alt = None
        logo_height = None

        comp = VerticalFormComponent(
            logo_src,
            logo_alt,
            logo_height,
            header_text,
            header_sub_text,
            controls,
            button_text,
            footer_text_lines,
            add_captcha=False,
            error_msg=self.error_message,
            css_id="newsletter",
        )

        return comp.render()

    @staticmethod
    def example():
        pass
