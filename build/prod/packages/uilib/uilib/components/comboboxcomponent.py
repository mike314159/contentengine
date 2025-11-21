from ..renderresponse import RenderResponse
from ..basecomponents import Component


class ComboBoxComponent(Component):

    def __init__(self, id, label, options, selected, post_url):
        self.id = id
        self.label = label
        self.options = options
        # self.value = value
        self.selected = selected
        self.post_url = post_url

    def render(self):

        # def generate_table_select_component(post_url, select_elements, selected_items):
        select_html = ""
        # for select_id, label_text, options in select_elements:

        select_html += f'<label for="{self.id}" class="me-2">{self.label}</label>'
        select_html += f'<select id="{self.id}" class="form-select me-4" name="{self.id}" hx-target="#rental-id" hx-indicator=".htmx-indicator" style="width: auto;">'
        for value, label in self.options:
            # selected_attr = ' selected' if self.id == selectedselected_items and selected_items[self.id] == value else ''
            selected_attr = ""
            select_html += f'<option value="{value}"{selected_attr}>{label}</option>'
        select_html += "</select>"

        html = f"""
            <div class="container mt-5">
                <div class="row">
                    <div class="col-12 d-flex justify-content-end">
                        <form class="d-flex align-items-center" action="{self.post_url}" method="POST">
                            {select_html}
                            <button type="submit" class="btn btn-primary">Submit</button>
                        </form>
                    </div>
                </div>
            </div>
        """
        return RenderResponse(html=html)
    
    @classmethod
    def example(cls):
        options = [
            ("option1", "Option 1"),
            ("option2", "Option 2"),
            ("option3", "Option 3"),
            ("option4", "Option 4")
        ]
        return cls(
            id="example-combo",
            label="Select an option:",
            options=options,
            selected="option2",
            post_url="/submit"
        )