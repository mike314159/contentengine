from ..renderresponse import RenderResponse
from ..basecomponents import Component


class FooterComponent(Component):
    def __init__(self, logo_src, logo_alt, footer_text, section_labels, sections):
        """
        Initialize the FooterComponent with dynamic content for customization.

        :param logo_src: The source URL for the logo image.
        :param logo_alt: The alternative text for the logo image.
        :param copyright_text: Copyright text to be displayed.
        :param section_labels: A list of labels for each section.
        :param sections: A list of lists, where each list contains tuples of URL and link text for that section.
        """
        self.logo_src = logo_src
        self.logo_alt = logo_alt
        self.footer_text = footer_text
        self.section_labels = section_labels
        self.sections = sections

    def render(self):
        # Helper function to build link lists
        def build_link_list(links):
            return "".join(
                f'<li class="mb-1"><a class="text-decoration-none footer-link" href="{url}">{text}</a></li>'
                for url, text in links
            )

        # Generate the HTML content for the footer component
        # <footer class="pt-4 my-md-5 pt-md-5 border-top footer mt-5">
        html = f"""
        <br><br>
        <footer class="footer mt-5">
            <div class="row">

            <div class="col-12 col-md">
                <img class="mb-2" src="{self.logo_src}" alt="{self.logo_alt}" width="50">
            </div>"""

        for label, section in zip(self.section_labels, self.sections):
            html += f"""
                <div class="col-6 col-md">
                    <h5 class='footer-links-header'>{label}</h5>
                    <ul class="list-unstyled text-small">
                    {build_link_list(section)}
                    </ul>
                </div>"""

        html += """</div>"""
        html += """<div class="row pt-4" style="text-align: center;">"""
        html += f"""<small class="d-block mb-3 text-muted">{self.footer_text}</small>"""
        # html += f'''<small class="d-block mb-3 text-muted">© {self.copyright_text}</small>'''
        html += """</div>"""
        html += """</footer>"""

        return RenderResponse(html=html)

    @staticmethod
    def example():

        # Example to instantiate and render the FooterComponent with custom links
        footer_component = FooterComponent(
            logo_src="/docs/5.0/assets/brand/bootstrap-logo.svg",
            logo_alt="Bootstrap Logo",
            footer_text="2017–2021",
            section_labels=["Section 1", "Section 2", "Section 3"],
            sections=[
                [("#", "Cool stuff"), ("#", "Random feature")],
                [("#", "Resource"), ("#", "Resource name")],
                [("#", "Team"), ("#", "Locations"), ("#", "Privacy"), ("#", "Terms")],
            ],
        )
        return footer_component