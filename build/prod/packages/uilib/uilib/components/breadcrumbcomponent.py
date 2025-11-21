from ..basecomponents import Component
from ..renderresponse import RenderResponse


class BreadCrumbComponent(Component):
    def __init__(self, crumbs):
        self.crumbs = crumbs

    def render(self):
        home = False
        html = ""
        html += "<nav aria-label='breadcrumb'>"
        html += "<ol class='breadcrumb'>"
        for label, url in self.crumbs:
            if url is None:
                html += "<li class='breadcrumb-item'>%s</li>" % (label)
            else:
                html += "<li class='breadcrumb-item'><a href='%s'>%s</a></li>" % (
                    url,
                    label,
                )
        html += "</ol>"
        html += "</nav>"

        # html += "<br>"
        # html += '''
        # <div class="btn-group btn-breadcrumb">
        #     <a href="#" class="btn btn-primary"><i class="bi bi-house" style="font-size: 1.5rem;"></i></a>
        #     <a href="#" class="btn btn-primary">Snippets</a>
        #     <a href="#" class="btn btn-primary">Breadcrumbs</a>
        #     <a href="#" class="btn btn-primary">Default</a>
        # </div>
        # '''

        return RenderResponse(html=html)
    
    @classmethod
    def example(cls):
        crumbs = [
            ("Home", "/"),
            ("Products", "/products"),
            ("Category", "/products/category"),
            ("Current Page", None)
        ]
        return cls(crumbs=crumbs)
