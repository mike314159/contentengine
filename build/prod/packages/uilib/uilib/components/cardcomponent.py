from ..basecomponents import Component
from ..renderresponse import RenderResponse


class CardComponent(Component):
    def __init__(
        self, title="Title", body="Yadda Yadda", button_label="Click Me", button_url="#"
    ):
        self.title = title
        self.body = body
        self.button_label = button_label
        self.button_url = button_url

    def render(self):
        html = """
            <div class="card">
            <div class="card-body">
                <h5 class="card-title">%s</h5>
                <p class="card-text">%s</p>
                <a href="%s" class="btn btn-primary">%s</a>
            </div>
            </div>
        """ % (
            self.title,
            self.body,
            self.button_url,
            self.button_label,
        )
        return RenderResponse(html=html)
    
    @classmethod
    def example(cls):
        return cls(
            title="Sample Card",
            body="This is a sample card component with some example content to demonstrate its functionality.",
            button_label="Learn More",
            button_url="/learn-more"
        )
