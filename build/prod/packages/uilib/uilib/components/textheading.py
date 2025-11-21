from ..basecomponents import Component
from ..renderresponse import RenderResponse


class TextHeading(Component):
    def __init__(self, text, level=3):
        self.text = text
        self.level = level

    def render(self):
        html = "<h%d>%s</h%d>" % (self.level, self.text, self.level)
        return RenderResponse(html=html)

    @staticmethod
    def example():
        text = "Example Text Heading"
        level = 3
        # Example usage of the TextHeading
        example_component = TextHeading(
            text=text,
            level=level,
        )
        return example_component