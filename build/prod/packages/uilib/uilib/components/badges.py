from ..basecomponents import Component
from ..renderresponse import RenderResponse


class Badges(Component):
    def __init__(self, badges_arr):
        self.badges = badges_arr

    def render(self):
        resp = RenderResponse()
        for b in self.badges:
            # h.append("<span class='badge bg-light text-dark'>%s</span>" % b)
            resp.add_html(
                "<button type='button' class='btn btn-secondary btn-md disabled' style='margin: 5px;'>%s</button>"
                % b
            )
        return resp

    @classmethod
    def example(cls):
        return cls(["Primary", "Secondary", "Success", "Danger", "Warning", "Info", "Light", "Dark"])
