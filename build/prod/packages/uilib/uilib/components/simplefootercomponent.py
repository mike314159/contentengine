from ..renderresponse import RenderResponse
from ..basecomponents import Component


class SimpleFooterComponent(Component):

    def __init__(self, site_name, links):
        self.links = links
        self.site_name = site_name

    def render(self):

        if len(self.links) == 0:
            links_body = ""
        else:
            links_html = ""
            for link in self.links:
                links_html += f'<li class="nav-item" style="padding: 10px; "><a href="{link["url"]}" class="footer-link">{link["name"]}</a></li>'

            links_body = f"""
                <ul class="nav justify-content-center">
                    {links_html}                
                </ul>
            """
        # <li class="nav-item"><a href="#" class="nav-link px-2 text-body-secondary">Home</a></li>
        html = f"""
            <footer class="footer pt-3 pb-2 mb-0">
                {links_body}
                <p class="text-center">© 2025 {self.site_name}</p>
            </footer>
            """
        return RenderResponse(html=html)

    @classmethod
    def example(cls):
        example_links = [
            {"name": "Home", "url": "/"},
            {"name": "About", "url": "/about"},
            {"name": "Contact", "url": "/contact"},
            {"name": "Privacy", "url": "/privacy"}
        ]
        return cls(site_name="Example Site", links=example_links)