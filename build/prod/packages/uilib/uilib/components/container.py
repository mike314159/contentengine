from ..basecomponents import Component
from ..renderresponse import RenderResponse


class ContainerRow(Component):
    def __init__(self, cols):
        self.num_cols = cols
        self.components = []

    def add_component(self, obj):
        self.components.append(obj)
        # print("Add Element ", obj)

    def is_full(self):
        return len(self.components) >= self.num_cols

    def render(self):
        resp = RenderResponse()
        resp.add_html("<div class='row'>")
        for e in self.components:
            if e is None:
                continue
            resp.add_html("<div class='col'>")
            if (type(e) == str) or (type(e) == int):
                resp.add_html(e)
            else:
                eresp = e.render()
                resp.add_response(eresp)
            resp.add_html("</div>")
        resp.add_html("</div>")
        return resp
    
    @classmethod
    def example(cls):
        row = cls(cols=3)
        from .htmlcomponent import HTMLComponent
        for i in range(1, 11):
            row.add_component(HTMLComponent(html=f"<div class='p-2 bg-light'>Item {i}</div>"))
        return row


class Container(Component):
    def __init__(self, cols, components=[], css_id=None, width=None):
        self.num_cols = cols
        self.row = 0
        self.rows = {}
        self.css_id = css_id
        for comp in components:
            self.add(comp)
        if width is not None:
            self.width_str = "style='width: %s;'" % width
        else:
            self.width_str = ""

    # def add_row(self):
    #    row_id = len(self.rows)
    #    self.rows[row_id] = []
    #    return row_id

    def add(self, obj):
        if self.row not in self.rows.keys():
            self.rows[self.row] = ContainerRow(self.num_cols)
        row = self.rows[self.row]
        if row.is_full():
            self.row += 1
            self.add(obj)
        else:
            row.add_component(obj)

    def render(self):
        if self.css_id is not None:
            css_id_str = "id='%s'" % self.css_id
        else:
            css_id_str = ""
        resp = RenderResponse()
        resp.add_html("<div class='container' %s %s>" % (css_id_str, self.width_str))
        #print("Rows: ", self.rows)
        for idx in self.rows.keys():
            row = self.rows[idx]
            row_resp = row.render()
            resp.add_response(row_resp)
        resp.add_html("</div>")
        return resp
    
    @classmethod
    def example(cls):
        from .htmlcomponent import HTMLComponent
        components = []
        for i in range(1, 11):
            components.append(HTMLComponent(html=f"<div class='p-2 bg-light'>Container Item {i}</div>"))
        return cls(cols=3, components=components)
