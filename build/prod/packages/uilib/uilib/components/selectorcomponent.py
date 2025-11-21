from ..renderresponse import RenderResponse
from ..basecomponents import Component


class SelectorComponent(Component):

    def __init__(self, id, label, options, selected_item_id, post_url):
        self.id = id
        self.label = label
        self.options = options
        self.selected_item_id = selected_item_id
        self.post_url = post_url

    def render(self):
        # Generate the select element HTML
        select_html = f'<label for="{self.id}" class="me-2">{self.label}</label>'
        select_html += f'<select id="{self.id}" class="form-select" style="width: auto;" onchange="window.location.href=this.value">'
        
        for item_id, value, label in self.options:
            selected_attr = ' selected' if item_id == self.selected_item_id else ''
            select_html += f'<option value="{value}"{selected_attr}>{label}</option>'
        select_html += "</select>"

        # Wrap in a container with flexbox alignment
        html = f"""
            <div class="container mt-3">
                <div class="row">
                    <div class="col-12 d-flex justify-content-end align-items-center">
                        {select_html}
                    </div>
                </div>
            </div>
        """
        
        return RenderResponse(html=html)
    
    @classmethod
    def example(cls):
        options = [
            ("option1", "/option1", "Option 1"),
            ("option2", "/option2", "Option 2"),
            ("option3", "/option3", "Option 3"),
            ("option4", "/option4", "Option 4")
        ]
        return cls(
            id="example-selector",
            label="Select an option:",
            options=options,
            selected_item_id="option2",
            post_url="/submit"
        )
