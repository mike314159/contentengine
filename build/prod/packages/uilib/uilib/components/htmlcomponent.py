from ..basecomponents import Component
from ..renderresponse import RenderResponse


class HTMLComponent(Component):
    def __init__(self, html="", footer_js=""):
        self.html = html
        self.footer_js = footer_js

    def render(self):
        return RenderResponse(html=self.html, footer_js=self.footer_js)
    
    @classmethod
    def example(cls):
        return cls(html="<div class='alert alert-info'><strong>HTML Component Example:</strong> This is a custom HTML component that can render any HTML content.</div>")
