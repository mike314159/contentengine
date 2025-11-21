from ..basecomponents import Component
from ..renderresponse import RenderResponse


class ButtonLinkComponent(Component):
    def __init__(self, text, url):
        self.text = text
        self.url = url

    def render(self):
        resp = RenderResponse()

        html = "<a class='btn btn-primary' href='%s' role='button'>%s</a>" % (
            self.url,
            self.text,
        )
        resp.add_html(html)
        # for b in self.badges:
        #     # h.append("<span class='badge bg-light text-dark'>%s</span>" % b)
        #     resp.add_html(
        #         "<button type='button' class='btn btn-secondary btn-md disabled' style='margin: 5px;'>%s</button>"
        #         % b
        #     )
        return resp
    
    @classmethod
    def example(cls):
        return cls(
            text="Example Button",
            url="/example"
        )
