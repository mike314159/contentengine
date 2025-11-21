from uilib.renderresponse import RenderResponse
from ..basecomponents import Component

class ListGroupComponent(Component):

    def __init__(self, css_id, items):
        self.css_id = css_id
        self.items = items
        self.first_col_width_pct = 15

    def __render(self):
        html = f'<table id="{self.css_id}" class="table table-bordered">'
        for row in self.items:
            html += '<tr>'
            for i, item in enumerate(row):
                if i == 0:
                    html += f'<td style="width: {self.first_col_width_pct}%;">'
                else:
                    html += '<td>'
                html += str(item)
                html += '</td>'
            html += '</tr>'
        html += '</table>'
        return RenderResponse(html=html)

    def render(self):
        html = '<p style="line-height: 1.9;">'
        for row in self.items:
            #html += '<tr>'
            for i, item in enumerate(row):
                item_str = "%s" % item
                if i == 0:
                    html += f"<b>{item_str}:&nbsp;</b>"
                else:
                    html += f"{item_str}"
            html += '<br>'
        html += '</p>'
        return RenderResponse(html=html)
    
    @staticmethod
    def example():
        url = "/"
        items = [
            ["Row1 Item1", "Row1 Item2"],
            ["Row2 Item1", "Row2 Item2"],
        ]
        return ListGroupComponent(css_id="example_list_group", items=items)