from ..basecomponents import Component
from ..renderresponse import RenderResponse


class CardsComponent(Component):

    def __init__(self, cards):
        self.cards = cards

    def example_data(self):
        cards = [
            (
                "Special title treatment",
                "With supporting text below as a natural lead-in to additional content.",
                "#",
                "Go",
            ),
            ("Another title", "More supporting text for another card.", "#", "Go"),
        ]
        return cards

    def render(self):
        card_html = ""
        for title, text, link, button_label in self.cards:
            card_html += f"""
<div class="col-sm-6">
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{title}</h5>
            <p class="card-text">{text}</p>
            <a href="{link}" class="btn btn-primary">{button_label}</a>
        </div>
    </div>
</div>
"""

        html = f"""
<div class="row">
  {card_html}
</div>
        """

        return RenderResponse(html=html, footer_js="")
    
    @classmethod
    def example(cls):
        cards = [
            ("Special title treatment", "With supporting text below as a natural lead-in to additional content.", "#", "Go"),
            ("Another title", "More supporting text for another card.", "#", "Go"),
            ("Third card", "This is the third card in the example.", "#", "Learn More")
        ]
        return cls(cards=cards)
