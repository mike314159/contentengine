from uilib.renderresponse import RenderResponse
from ..basecomponents import Component


class PricingPlansComponent(Component):
    def __init__(self, title, description, plans, left_justified=False):
        """
        Initialize the PricingPlansComponent with a list of pricing plans.
        Each plan in the list should be a dictionary with keys for plan_name, price, features, button_text, and highlighted (optional).

        :param plans: A list of dictionaries, each representing a pricing plan.
        """
        self.title = title
        self.description = description
        self.plans = plans
        self.left_justified = left_justified

    def _get_card_html(self, title, price, period, features, button_text, button_url, badge_text):

        features_html = ""
        for feature in features:
            features_html += f"<li class='mb-3 d-flex align-items-center'><i class='bi bi-check-circle-fill text-primary me-2'></i>{feature}</li>"

        popular_badge = f"<span class='badge bg-primary-subtle text-primary mb-3'>{badge_text}</span>"    

#                    <div class="position-absolute top-0 start-0 w-100 bg-primary opacity-10" style="height: 8px;"></div>

        card_html = f"""
            <div class="col-lg-4 col-md-6">
                <div class="card h-100 shadow-lg border-0 pricing-card position-relative overflow-hidden">
                    <div class="card-body p-3">
                        {popular_badge}
                        <h3 class="fw-bold mb-4">{title}</h3>
                        <div class="mb-4">
                            <span class="display-6 fw-bold">{price}</span>
                            <span class="text-muted">/{period}</span>
                        </div>
                        <ul class="list-unstyled mb-4">
                            {features_html}
                        </ul>
                        <a href="{button_url}" class="btn btn-primary w-100 py-3 fw-semibold">{button_text}</a>
                    </div>
                </div>
            </div>
        """
                    # <div class="card-footer bg-light border-0 p-4">
                    #     <p class="text-center mb-0 text-muted">
                    #         <small>Cancel anytime. No questions asked.</small>
                    #     </p>
                    # </div>


        return card_html
    
    def render(self):
        # Begin the container for the pricing plans


        # cards = []
        # # Loop through each plan and construct its card HTML
        # for plan in self.plans:
        #     # Check if the plan is highlighted
        #     card_class = "mb-4 rounded-3 shadow-sm pricing-card border-primary"
        #     card_class = "mb-4 shadow-sm pricing-card border-primary"
        #     card_class = "pricing-card border-primary"
        #     header_class = "pricing-card-header py-2"
        #     button_class = "w-75 btn btn-md btn btn-primary pt-2 pb-2"
        #     #if plan.get("highlighted", False):
        #     #card_class += " border-primary"
        #     #header_class += " text-white bg-primary border-primary"
        #     #button_class = "w-100 btn btn-lg btn-primary"

        #     plan_name = plan['plan_name']
        #     price = plan['price']
        #     features = plan['features']
        #     button_text = plan['button_text']
        #     button_url = plan['button_url']

        #     # Construct the plan card
        #     card_html = f"""
        #     <div class="col-md-4 {card_class}" style="margin-left: 10px; margin-right: 10px;">
        #         <div class="{header_class} w-100">
        #             <div class="my-0 fw-normal">{plan_name}</div>
        #         </div>
        #         <div class="pricing-card-body mt-3">
        #             <div class="pricing-card-price">{price}
        #             </div>
        #             <ul class="list-unstyled mt-2 mb-4 pricing-card-features">
        #                 {''.join(f"<li>{feature}</li>" for feature in features)}
        #             </ul>
        #             <a type="button" class="{button_class} active btn-md" href="{button_url}">{button_text}</a>
        #         </div>
        #     </div>
        #     """
        #     cards.append(card_html)
        # cards_html = ''.join(cards)

        # if self.left_justified:
        #     header_html = f"""
        #     <div class="row pricing-header pb-md-4 pt-3">
        #         <div class="col-12 text-start" style="text-align: left;">
        #             <div class="pricing-card-title text-start" style="text-align: left;">
        #                 <h2><a name="pricing">{self.title}</a></h2>
        #             </div>
        #             <div class="pricing-card-subtitle text-start" style="text-align: left;">
        #                 <p>{self.description}</p>
        #             </div>
        #         </div>
        #     </div>
        #     """
        #     html = f"""
        #         {header_html}
        #         </div>
        #         <div class="row row-cols-1 row-cols-md-3 mb-3 text-center ">
        #             {cards_html}
        #         </div>
        #     """

        # else:
        #     header_html = f"""
        #     <div class="row pricing-header p-3 pb-md-4 mx-auto text-center">
        #         <div class="pricing-card-title">
        #             <h2><a name="pricing">{self.title}</a></h2>
        #         </div>
        #         <div class="pricing-card-subtitle">
        #             <p>{self.description}</p>
        #         </div>
        #     </div>
        #     """
        #     html = f"""
        #         {header_html}
        #         </div>
        #         <div class="row row-cols-1 row-cols-md-3 mb-3 text-center justify-content-center">
        #             {cards_html}
        #         </div>
        # """
            
        cards = []  
        for plan in self.plans:
            plan_name = plan['plan_name']
            price = plan['price']
            period = plan['period']
            features = plan['features']
            button_text = plan['button_text']
            button_url = plan['button_url']
            badge_text  = plan['badge_text']
            card_html = self._get_card_html(title=plan_name, price=price, period=period, 
                                            features=features, button_text=button_text, 
                                            button_url=button_url, badge_text=badge_text)
            cards.append(card_html)
        cards_html = '\n'.join(cards)

        # html = f"""
        #     {header_html}
        #     <div class="row row-cols-1 row-cols-md-3 mb-3 text-center">
        #         {cards_html}
        #     </div>
        # """

        header_html = f"""
            <div class="row pricing-header p-3 pb-md-4 mx-auto text-center">
                <div class="pricing-card-title">
                    <h2><a name="pricing">{self.title}</a></h2>
                </div>
                <div class="pricing-card-subtitle">
                    <p>{self.description}</p>
                </div>
            </div>
            """
        

        html = f"""
            <div class="container py-2">
                {header_html}
                <div class="row g-4 justify-content-center">
                    {cards_html}
                </div>
            </div>
        """
        return RenderResponse(html=html)

    @classmethod
    def example(cls):
        # Example usage of the PricingPlansComponent
        example_plans = [
            {
                "plan_name": "Free",
                "price": "$0",
                "period": "month",
                "features": [
                    "10 users included",
                    "2 GB of storage",
                    "Email support",
                    "Help center access",
                ],
                "button_text": "Sign up for free",
                "button_url": "/signup",
                "badge_text": "Basic",
                "highlighted": False,
            },
            {
                "plan_name": "Pro",
                "price": "$15",
                "period": "month",
                "features": [
                    "20 users included",
                    "10 GB of storage",
                    "Priority email support",
                    "Help center access",
                ],
                "button_text": "Get started",
                "button_url": "/pro-signup",
                "badge_text": "Popular",
                "highlighted": True,
            },
            {
                "plan_name": "Enterprise",
                "price": "$29",
                "period": "month",
                "features": [
                    "30 users included",
                    "15 GB of storage",
                    "Phone and email support",
                    "Help center access",
                ],
                "button_text": "Contact us",
                "button_url": "/contact",
                "badge_text": "Advanced",
                "highlighted": False,
            },
        ]
        example_component = cls(title="Choose Your Plan", description="Select the perfect plan for your needs", plans=example_plans)
        return example_component

