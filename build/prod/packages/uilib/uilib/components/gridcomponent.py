from ..basecomponents import Component
from ..renderresponse import RenderResponse


class GridComponent(Component):
    def __init__(self, col_style="col-4", num_cols=3):
        super().__init__()
        self.rows = {1: []}
        self.current_row = 1
        self.num_cols = num_cols
        self.col_style = col_style

    def add(self, compopnent):
        if len(self.rows[self.current_row]) >= self.num_cols:
            self.current_row += 1
        if self.current_row not in self.rows.keys():
            self.rows[self.current_row] = []
        html = compopnent.render().get_html()
        self.rows[self.current_row].append(html)

    def _render_row(self, cols):
        cells = ["<div class='row'>"]
        for cell_html in cols:
            html = """
                <div class="%s">
                    %s
                </div>
            """ % (
                self.col_style,
                cell_html,
            )
            cells.append(html)
        cells.append("</div>")
        return "".join(cells)

    def render(self):
        rows = []
        for row in range(1, self.current_row + 1):
            row_html = self._render_row(self.rows[row])
            rows.append(row_html)
        html = "<div class='container'>"
        html += "".join(rows)
        html += "</div>"
        return RenderResponse(html=html)
    
    @classmethod
    def example(cls):
        grid = cls(col_style="col-4", num_cols=3)
        # Add some sample content to the grid
        from .htmlcomponent import HTMLComponent
        grid.add(HTMLComponent(html="<div class='p-2 bg-light'>Item 1</div>"))
        grid.add(HTMLComponent(html="<div class='p-2 bg-light'>Item 2</div>"))
        grid.add(HTMLComponent(html="<div class='p-2 bg-light'>Item 3</div>"))
        grid.add(HTMLComponent(html="<div class='p-2 bg-light'>Item 4</div>"))
        return grid
