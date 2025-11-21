from ..renderresponse import RenderResponse
from ..basecomponents import Component


class PrivacyPolicyComponent(Component):
    def __init__(self, file_path, home_url, company_name, contact_url):
        # Store the path to the HTML file and the company name to insert.
        self.file_path = file_path
        self.home_url = home_url
        self.contact_url = contact_url
        self.company_name = company_name

    def render(self):
        # Read the HTML file content
        try:
            with open(self.file_path, "r") as file:
                html_content = file.read()
        except FileNotFoundError:
            return RenderResponse(html="Error: File not found.", footer_js="")

        # Replace placeholder with the actual company name
        html_content = html_content.replace("{home_url}", self.home_url)
        html_content = html_content.replace("{company_name}", self.company_name)
        html_content = html_content.replace("{contact_url}", self.contact_url)

        # Since this component might not use JavaScript, we set it as an empty string
        javascript = ""

        return RenderResponse(html=html_content, footer_js=javascript)

    @classmethod
    def example(cls):
        # Provide an example usage of the PrivacyPolicyComponent.
        file_path = "/packages/uilib/uilib/statics/templates/privacy_policy.html"
        home_url = "https://example.com"
        company_name = "Example Company"
        contact_url = "https://example.com/contact"
        component = cls(file_path, home_url, company_name, contact_url)
        return component