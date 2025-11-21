
from uilib.renderresponse import RenderResponse
from ..basecomponents import Component

class HeroComponent(Component):
    def __init__(
        self,
        logo_src=None,
        title="Test Title",
        subtitle="Test Subtitle",
        primary_button_text=None,
        primary_button_url=None,
        secondary_button_text=None,
        secondary_button_url=None,
        image_src=None,
        image_alt=None,
        logo_width="72",
    ):
        self.title = title
        self.subtitle = subtitle
        self.primary_button_text = primary_button_text
        self.primary_button_url = primary_button_url
        self.secondary_button_text = secondary_button_text
        self.secondary_button_url = secondary_button_url
        self.image_src = image_src
        self.image_alt = image_alt
        self.logo_src = logo_src
        self.logo_width = logo_width

    def render(self):
        # Generate the HTML content for the hero component

        if self.logo_src is not None:
            logo_html = f"""<img class="d-block mx-auto mb-4" src="{self.logo_src}" alt="" width="{self.logo_width}" >"""
        else:
            logo_html = ""

        if (self.primary_button_text is not None) and (
            self.primary_button_url is not None
        ):
            first_button_html = f'<a type="button" class="btn btn-primary btn-lg px-4 me-sm-3 active" href="{self.primary_button_url}">{self.primary_button_text}</a>'
        else:
            first_button_html = ""

        second_button_html = (
            f'<button type="button" class="btn btn-outline-secondary btn-lg px-4">{self.secondary_button_text}</button>'
            if self.secondary_button_text is not None
            else ""
        )

        if self.image_src is not None:
            image_html = f'<img src="{self.image_src}" class="img-fluid border rounded-3 shadow-lg mb-4" alt="{self.image_alt}" width="700" height="500" loading="lazy">'
        else:
            image_html = ""

        # Conditionally render title
        title_html = ""
        if self.title is not None:
            title_html = f"""<h1 class="hero-title">
                {self.title}
            </h1>"""

        html = f"""
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8 px-4 pt-3 my-3 text-center">
            {logo_html}
            {title_html}
            <p class="mb-4 mt-3 hero-subtitle">
                {self.subtitle}
            </p>
            <div class="justify-content-sm-center mt-4 mb-3">
                {first_button_html}
                {second_button_html}
            </div>
            <div>
                {image_html}
            </div>
        </div>
    </div>
</div>
"""
        return RenderResponse(html=html)

    @staticmethod
    def example():

        logo_src = "/statics/bootstrap-logo.svg"

        # Example usage of the HeroComponent
        example_component = HeroComponent(
            logo_src=logo_src,
            title="Centered screenshot",
            subtitle="Quickly design and customize responsive mobile-first sites with Bootstrap, the world’s most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, extensive prebuilt components, and powerful JavaScript plugins.",
            primary_button_text="Primary button",
            secondary_button_text="Secondary",
            image_src="bootstrap-docs.png",
            image_alt="Example image",
        )
        return example_component

