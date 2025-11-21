

class RenderResponse:
    def __init__(self, html=None, footer_js=None, css_links=None, header_js=None):
        self.html = []
        self.header_js = []
        self.footer_js = []
        self.css_links = []
        if html is not None:
            self.add_html(html)
        if header_js is not None:
            self.add_header_js(header_js)
        if footer_js is not None:
            self.add_footer_js(footer_js)
        if css_links is not None:
            self.add_css_links(css_links)

    def add_html(self, html):
        self.html.append(html)

    def add_footer_js(self, footer_js):
        self.footer_js.append(footer_js)

    def add_css_links(self, css_link):
        self.css_links.append(css_link)

    def add_header_js(self, header_js):
        self.header_js.append(header_js)

    def get_html(self):
        return "\n".join(self.html)

    def get_footer_js(self):
        return "\n".join(self.footer_js)

    def get_css_links(self):
        return "\n".join(self.css_links)

    def get_header_js(self):
        return "\n".join(self.header_js)

    def add_response(self, resp):
        self.add_html(resp.get_html())
        self.add_header_js(resp.get_header_js())
        self.add_footer_js(resp.get_footer_js())
        self.add_css_links(resp.get_css_links())

    def get_html(self):
        return "\n".join(self.html)

