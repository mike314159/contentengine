from ..basecomponents import Component
from ..renderresponse import RenderResponse


class PageHeaderComponent2(Component):
    def __init__(self, title, attrs=None):
        self.title = title
        # self.name = name
        self.attrs = attrs

    # def css_style(self, attrs):
    #     s = []
    #     for k, v in attrs.items():
    #         s.append("%s: %s;" % (k, v))
    #     return " ".join(s)

    def render(self):
        #     cat_attrs = {
        #         "font-size": "18px",
        #         "color": "#909497",
        #         "font-weight": "600",
        #         "margin-top": "0px",
        #         "margin-bottom": "0px",
        #     }
        #     item_attrs = {
        #         "font-weight": "600",
        #         "color": "#555555",
        #     }
        #     style_cat = self.css_style(cat_attrs)
        #     style_item = self.css_style(item_attrs)
        #     html = "<br><span style='%s'><p>%s</p><p style='%s'>%s</p></span>" % (
        #         style_cat,
        #         self.category,
        #         style_item,
        #         self.name,
        #     )
        html = "<h1>%s</h1>" % self.title
        if self.attrs is not None:
            for k, v in self.attrs.items():
                html += "%s: %s<br>" % (k, v)
        html += "<br>"
        return RenderResponse(html=html)
