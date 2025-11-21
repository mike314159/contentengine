from ..renderresponse import RenderResponse
from ..basecomponents import Component


class HeaderJsComponent(Component):

    def __init__(self, header_js):
        self.header_js = header_js

    def render(self):
        return RenderResponse(header_js=self.header_js)
