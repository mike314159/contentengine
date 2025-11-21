from ..renderresponse import RenderResponse
from ..basecomponents import Component


class AccordionComponent(Component):
    def __init__(self, header, accordion_id, sections):
        """
        Initialize the AccordionComponent with dynamic sections for customization.

        :param accordion_id: The ID for the entire accordion component to ensure uniqueness in the DOM.
        :param sections: A list of dictionaries, each containing a 'title' and 'content' for each accordion item.
        """
        self.accordion_id = accordion_id
        self.sections = sections
        self.header = header

    def render(self):
        # Generate the HTML content for the accordion component
        html = f'<div class="accordion" id="{self.accordion_id}">'
        for index, section in enumerate(self.sections, start=1):
            is_expanded = "true" if index == 1 else "false"
            show_class = "show" if index == 1 else ""
            panel_id = f"{self.accordion_id}-collapse{index}"
            header_id = f"{self.accordion_id}-heading{index}"

            html += f"""
  <div class="accordion-item">
    <h2 class="accordion-header" id="{header_id}">
      <button class="accordion-button {'collapsed' if index != 1 else ''}" type="button" data-bs-toggle="collapse" data-bs-target="#{panel_id}" aria-expanded="{is_expanded}" aria-controls="{panel_id}">
        {section['title']}
      </button>
    </h2>
    <div id="{panel_id}" class="accordion-collapse collapse {show_class}" aria-labelledby="{header_id}">
      <div class="accordion-body">
        {section['content']}
      </div>
    </div>
  </div>"""
        html += "</div>"

        html = f"""
            <h1>{self.header}</h1>
            <br>
            {html}
        """
        return RenderResponse(html=html)

    @staticmethod
    def example():
        # Example usage of the AccordionComponent
        accordion_component = AccordionComponent(
            header="Example Accordion",
            accordion_id="accordionPanelsStayOpenExample",
            sections=[
                {
                    "title": "Accordion Item #1",
                    "content": "This is the first item's accordion body.",
                },
                {
                    "title": "Accordion Item #2",
                    "content": "This is the second item's accordion body.",
                },
                {
                    "title": "Accordion Item #3",
                    "content": "This is the third item's accordion body.",
                },
            ],
        )

        return accordion_component