from ..basecomponents import Component
from ..renderresponse import RenderResponse


class TabsComponent(Component):
    def __init__(self, tabs, selected_id, view='tabs', aligned_right=True):
        self.tabs = tabs
        self.selected_id = selected_id
        self.view = view
        self.aligned_right = aligned_right

    def render(self):
        # Add custom CSS for darker borders
        css = """
            <style>
                .nav-tabs {
                    border-bottom: 1px solid #dee2e6;
                }
                .nav-tabs .nav-link {
                    border-color: #f8f9fa #f8f9fa #dee2e6;
                    color: #6c757d;
                    border: 1px solid transparent;
                    margin-bottom: -1px;
                }
                .nav-tabs .nav-link.active {
                    border-color: #AAAAAA;
                    border-bottom: 0px;
                    color: #495057;
                    font-weight: 500;
                    background-color: #f8f9fa;
                }
                .nav-tabs .nav-link:hover:not(.active) {
                    border-color: border-color: #AAAAAA;
                    isolation: isolate;
                }
            </style>
        """

        # Add justify-content-end class if aligned_right is True
        alignment_class = " justify-content-end" if self.aligned_right else ""

        if self.view == 'pills':
            html = f"<ul class='nav nav-pills{alignment_class}'>"
        else:
            html = css + f"<ul class='nav nav-tabs{alignment_class}'>"

        for id, label, link in self.tabs:
            html += "<li class='nav-item'>"
            if id == self.selected_id:
                html += (
                    "<a class='nav-link active' aria-current='page' href='%s'>%s</a>"
                    % (link, label)
                )
            else:
                html += "<a class='nav-link' href='%s'>%s</a>" % (link, label)
            html += "</li>"
        html += "</ul>"
        return RenderResponse(html=html)

    @classmethod
    def example(cls):
        example_tabs = [
            ("home", "Home", "/"),
            ("about", "About", "/about"),
            ("contact", "Contact", "/contact"),
            ("services", "Services", "/services")
        ]
        return cls(tabs=example_tabs, selected_id="home", view='tabs', aligned_right=True)

    # def render(self):
    #     tabs = []
    #     #view_info = []
    #     #for view in views:
    #     #    view_info.append((view, view))
    #     #for view in view_info:
    #     #    selected = view[1] == selected_view
    #     #    url = url_for("dataset_page", dataset_id=dataset_id, view=view[1])
    #     #    tabs.append({"label": view[0], "link": url, "selected": selected})
    #     tabs_html = render_tabs(tabs)
    #     return tabs_html
