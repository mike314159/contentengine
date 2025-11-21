from ..basecomponents import Component
from ..renderresponse import RenderResponse


class ComponentStack(Component):
    def __init__(self):
        super().__init__()
        self.components = []

    def add(self, compopnent):
        self.components.append(compopnent)

    def render(self):
        response = RenderResponse()
        for component in self.components:
            r = component.render()
            response.add_response(r)
        return response
    
    @classmethod
    def example(cls):
        stack = cls()
        from .htmlcomponent import HTMLComponent
        from .buttoncomponent import ButtonComponent
        from .cardcomponent import CardComponent
        
        # Component 1: Header
        stack.add(HTMLComponent(html="<h3>Component Stack Example</h3>"))
        
        # Component 2: Description paragraph
        stack.add(HTMLComponent(html="<p>This is a component stack that can hold multiple components. Each component is numbered and stacked vertically.</p>"))
        
        # Component 3: Info alert
        stack.add(HTMLComponent(html="<div class='alert alert-info'><strong>Component 3:</strong> This is an HTML component with Bootstrap styling!</div>"))
        
        # Component 4: Button
        stack.add(ButtonComponent(
            label="Component 4 - Click Me",
            url="/example",
            btn_style="btn-success",
            btn_size="btn-md"
        ))
        
        # Component 5: Card
        stack.add(CardComponent(
            title="Component 5 - Sample Card",
            body="This is a card component demonstrating how different UI elements can be stacked together in a ComponentStack.",
            button_label="Learn More",
            button_url="/learn-more"
        ))
        
        return stack
