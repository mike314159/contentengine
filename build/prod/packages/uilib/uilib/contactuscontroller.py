import json
from flask import url_for
import bleach
from uilib.components import ContactUsComponent
from uilib.components import FormConfirmationComponent
#from siteconfig import SiteConfig

class ContactUsController:

    def __init__(self, contact_us_db, analytics, captcha_image_src):
        self.contact_us_db = contact_us_db
        self.analytics = analytics
        self.post_url = url_for("site_contact_us_page")
        self.cancel_url = url_for("site_home_page")
        self.captcha_image_src = captcha_image_src
        print("Controller Captcha image src:", self.captcha_image_src)
        #self.analytics_event_name = 'contact_form'

    def sanitize_message(self, message):
        return bleach.clean(message, tags=[], attributes={})

    # def validate_contact_form(form_attrs):
    #     email = form_attrs.get("email", None)
    #     message = form_attrs.get("message", None)
    #     captcha_code = form_attrs.get("captcha", None)
    #     if not is_valid_captcha(request, captcha_code):
    #         return (email, message, "ERROR: Invalid captcha code, try again.")
    #     if not valid_email(email):
    #         return (email, message, "ERROR: Invalid email address")
    #     if not valid_msg(message):
    #         return (email, message, "ERROR: Invalid message")
    #     return (email, message, None)

    def process_request(self, request):
        #print("Process request Captcha image src:", self.captcha_image_src)
        msg = None
        form_attrs = {}
        if request.method == "POST":
            form_attrs = request.form
            print("Form Attrs:", json.dumps(form_attrs, indent=4))

        form_comp = ContactUsComponent(
            logo_src=None,
            form_attrs=form_attrs,
            # error_message=error_msg,
            post_url=url_for("site_contact_us_page"),
            cancel_url=url_for("site_home_page"),
            captcha_image_src=self.captcha_image_src,
        )
        #print("ContactUsComponent created")

        if request.method == "POST":

            #form_comp.validate()
            #form_valid = form_comp.is_valid(request)

            form_valid = form_comp.validate_form(request)

            if not form_valid:
                self.analytics.log_event(
                    object='app',
                    verb="contact_form_invalid",
                    request=request,
                    properties={}
                )
                                
            if form_valid:

                from_user_email = form_comp.get_email()
                message = form_comp.get_message()
                # code = form_comp.get_captcha_code()
                # sanitized_message = self.sanitize_message(message)

                success = self.contact_us_db.add(
                    name=None,
                    email=from_user_email,
                    message=message,
                )
                self.analytics.log_event(
                    object='app',
                    verb="contact_form_message",
                    request=request,
                    properties={"success": int(success), "email": from_user_email}
                )

                if success:
                    comp = FormConfirmationComponent(
                        header_text="Contact Us",
                        header_sub_text="<b>Message Sent.</b><br><br>Thanks for the feedback! We will get back to you soon.",
                        button_text="Return to Home",
                        button_url="/",
                    )
                    return comp, None
                else:
                    err_msg = "Message Failed. Please try again later."
                    form_comp.form_component.set_error_message(err_msg)

        redirect_url = None
        return form_comp, redirect_url
    