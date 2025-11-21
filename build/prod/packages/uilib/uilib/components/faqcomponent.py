from uilib.renderresponse import RenderResponse
from ..basecomponents import Component


class FAQComponent(Component):
    def __init__(
        self,
        contact_url,
        title="FAQs",
        subtitle="Got questions? We've got answers.",
        questions=[], # a list of tuples of (question, answer)
    ):
        self.title = title
        self.subtitle = subtitle
        self.questions = questions
        self.contact_url = contact_url
    def render(self):
        # Generate the HTML content for the hero component

        # if self.logo_src is not None:
        #     logo_html = f"""<img class="d-block mx-auto mb-4" src="{self.logo_src}" alt="" width="{self.logo_width}" >"""
        # else:
        #     logo_html = ""

        # if (self.primary_button_text is not None) and (
        #     self.primary_button_url is not None
        # ):
        #     first_button_html = f'<a type="button" class="btn btn-primary btn-lg px-4 me-sm-3 active" href="{self.primary_button_url}">{self.primary_button_text}</a>'
        # else:
        #     first_button_html = ""

        # second_button_html = (
        #     f'<button type="button" class="btn btn-outline-secondary btn-lg px-4">{self.secondary_button_text}</button>'
        #     if self.secondary_button_text is not None
        #     else ""
        # )

        # if self.image_src is not None:
        #     image_html = f'<img src="{self.image_src}" class="img-fluid border rounded-3 shadow-lg mb-4" alt="{self.image_alt}" width="700" height="500" loading="lazy">'
        # else:
        #     image_html = ""

        button_html = f'<a type="button" class="btn btn-outline-secondary btn-md px-4" href="{self.contact_url}">Contact Us</a>'

        qa = []
        for question, answer in self.questions:
            tmpl = f"""
                <h2 class="mb-3">Q. {question}</h2>
                <p class="text-muted">{answer}</p>
                """
            qa.append(tmpl)

        questions_html = "".join(qa)
        html = f"""
        <h1 class="hero-title text-center">{self.title}</h1>
        <p class="mb-4 hero-subtitle text-center">{self.subtitle}</p>
        <div class="pt-1 my-5 text-justify">
            <div class="justify-content-sm-left mb-5" style="line-height: 1.85;">
                {questions_html}
            </div>
            <p>Any additional questions?</p>
            {button_html}
        </div>
        """
        return RenderResponse(html=html)
    
    @classmethod
    def example(cls):
        questions = [
            ("What is this service?", "This is a sample FAQ component that demonstrates how to display frequently asked questions and answers."),
            ("How do I get started?", "Simply follow the instructions provided in the documentation to begin using our service."),
            ("Is there a free trial?", "Yes, we offer a 30-day free trial for all new users to test our features."),
            ("How can I contact support?", "You can reach our support team through the contact form or by emailing support@example.com.")
        ]
        return cls(
            contact_url="/contact",
            title="Frequently Asked Questions",
            subtitle="Find answers to common questions about our service.",
            questions=questions
        )

