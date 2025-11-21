from ..renderresponse import RenderResponse
from ..basecomponents import Component


class ButtonComponent(Component):

    def __init__(self, label, url, btn_style="btn-primary", btn_size="btn-md", css_style="", active=False):
        self.label = label
        self.url = url
        self.btn_style = btn_style
        self.btn_size = btn_size
        self.css_style = css_style
        if active:
            self.active = "active"
        else:
            self.active = ""

    def get_html(self):
        return f'<a href="{self.url}" class="btn btn-{self.btn_style} {self.btn_size} {self.active}" style="{self.css_style}">{self.label}</a>'

    def render(self):
        return RenderResponse(html=self.get_html())
    
    @classmethod
    def example(cls):
        return cls(
            label="Click Me",
            url="/example",
            btn_style="btn-primary",
            btn_size="btn-md"
        )
