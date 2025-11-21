from ..renderresponse import RenderResponse
from ..basecomponents import Component


class NewsletterSubscribeComponent(Component):

    def __init__(self, prefix_text, html=None, sub_title=None, bg_color="#152f3f"):
        self.prefix_text = prefix_text
        self.html = html
        self.bg_color = bg_color
        self.sub_title = sub_title

    def render(self):
        if self.sub_title is not None:
            sub_title_html = f"""
                <div class="d-flex justify-content-center mt-3 text-center mx-auto" style="width: 80%;">
                    <span class="me-3" style="font-size: 0.9rem;">{self.sub_title}</span>
                </div>
            """
        else:
            sub_title_html = ""

        html = f"""
            <div class="pt-3 pb-3 mt-5 mb-0 newsletter">
                <div class="d-flex align-items-center justify-content-center">
                    <span class="me-3" style="font-size: 1.3rem;">{self.prefix_text}</span>
                    {self.html}
                </div>
                {sub_title_html}
            </div>
            """
        return RenderResponse(html=html)
    
    @classmethod
    def example(cls):
        from .htmlcomponent import HTMLComponent
        form_html = HTMLComponent(html='''
            <form class="d-inline-flex">
                <input type="email" class="form-control me-2" placeholder="Enter your email" style="width: 250px;">
                <button type="submit" class="btn btn-primary">Subscribe</button>
            </form>
        ''')
        return cls(
            prefix_text="Stay updated with our newsletter:",
            html=form_html.render().get_html(),
            sub_title="Get the latest news and updates delivered to your inbox."
        )