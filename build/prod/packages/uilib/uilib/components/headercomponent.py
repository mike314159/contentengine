from uilib.renderresponse import RenderResponse
from ..basecomponents import Component
import json

"""

Write the code for a python class that renders an HTML template for a component on a website.
    
Here is an example of a component that is simply an HTML heading. Use this design for all components you write.

class HeadingComponent(Component):
    def __init__(self, text):
        # All necessary parameters are passed into the constructor and stored in the class instance.
        # :param text: The text to display inside the <h1> tag.
        self.text = text

    def render(self):
        # Fills in values of the template and returns a RenderResponse object.
        # :return: A string containing HTML for the <h1> tag.
        html = f'<h1>{self.text}</h1>'
        javascript = ''
        return RenderResponse(html=html, footer_js=javascript)

    @staticmethod
    def example():
        # Provides an instance of an example of the HeadingComponent.
        # :return: A string containing example HTML for the heading.
        text = "Example Header"
        component = HeadingComponent(text)
        return component

Inspect the template and create parameters for all the values that will likely need to be filled for multiple different uses of this component in the future. 
Do not explain the code or give me examples on how to use it. Just return the code. 

Here is the raw HTML I want you to use for a new component called ZZZZ
HHHHHHHHHHHHHHHH
"""


class HeaderComponent(Component):
    def __init__(
        self,
        site_name,
        logo_src,
        logo_height,
        home_page_url,
        #links,
        #login_url,
        #sign_up_url,
        #sign_out_url,
        current_item=None,
        #buttons=[], 

        # These links appear on the right side of the header
        links = {},# expecting tuple list of (text, url),

        # These links appear centered in the header
        center_links = {},# expecting tuple list of (text, url),
        drop_down_menu_links = {},# expecting tuple list of (text, url),
        drop_down_menu_label = None,
    ):
        self.home_page_url = home_page_url
        #self.links = links
        #self.login_url = login_url
        #self.sign_up_url = sign_up_url
        self.current_item = current_item
        #self.sign_out_url = sign_out_url
        self.site_name = site_name
        self.logo_src = logo_src
        self.logo_alt_text = site_name
        self.logo_height = logo_height
        #self.buttons = buttons
        self.links = links
        self.center_links = center_links
        self.drop_down_menu_label = drop_down_menu_label
        self.drop_down_menu_links = drop_down_menu_links

    # def _render_buttons_html(self):
    #     b = []
    #     for (text, url) in self.buttons:
    #         if text is not None and url is not None:
    #             html = f"""<a type="button" href='{url}'" class="btn btn-outline-primary me-2 header-login-button">{text}</a>"""
    #             b.append(html)
    #     return "".join(b)

    def link_tmpl(self, text, url, link_type='link', active=False, bold=False, size_em=None):
        if bold:
            bold_class = "fw-bold"
        else:
            bold_class = ""
        if size_em is not None:
            size_style = f"style='font-size: {size_em}em;'"
        else:
            size_style = ""

        if link_type == 'link':
            html = f"""
                <li class="nav-item active">
                    <a class="nav-link me-2 {bold_class}" {size_style} href="{url}">{text}</a>
                </li>
            """
        elif link_type == 'button':
            active_class = "active" if active else ""
            html = f"""
                <li class="nav-item">
                    <a type="button" href='{url}' class="btn btn-outline-primary me-2 {active_class}">{text}</a>
                </li>
            """
        else:
            raise ValueError(f"Invalid link type: {link_type}")
        return html
    
    def dropdown_link_tmpl(self, text, url, link_type='link'):
        if link_type == 'link':
            html = f"""
                <a class="dropdown-item" href="{url}">{text}</a>
            """
        elif link_type == 'button':
            html = f"""
                <button class="dropdown-item" onclick="window.location.href='{url}'">{text}</button>
            """
        elif link_type == 'divider':
            html = """<li><hr class="dropdown-divider"></li>"""
        else:
            raise ValueError(f"Invalid link type: {link_type}")
        return html

    def dropdown_tmpl(self, dropdown_link_text, dropdown_links):
        dropdown_links_html = ""
        for link in dropdown_links:
            name = link.get("name", None)
            url = link.get("url", None)
            link_type = link.get("type", 'link')
            dropdown_links_html += self.dropdown_link_tmpl(name, url, link_type)

        html = f"""
         <li class="nav-item dropdown">
          <button type="button" class="btn dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
            {dropdown_link_text}
            </button>
           <ul class="dropdown-menu">
             {dropdown_links_html}
           </ul>
         </li>
        """

        return html

    def generate_links_html(self, links, bold=False, size_em=None):
        #print("Generate Links HTML")
        #print(json.dumps(links, indent=4))

        links_html = ""
        for link in links:
            url = link.get("url", None)
            if url is not None:
                name = link.get("name", None)
                links_html += self.link_tmpl(
                    name, 
                    link["url"], 
                    link.get("type", 'link'), 
                    link.get("active"), 
                    bold, 
                    size_em
                )
            # else:
            #     links_html = """<li><hr class="dropdown-divider"></li>"""

            dropdown_links = link.get("links", None)
            if dropdown_links is not None:
                dropdown_html = self.dropdown_tmpl(link["name"], dropdown_links)
                links_html += dropdown_html  
        return links_html              

    def _render_dropdown_links_html(self, menu_label, menu_links):
        if len(menu_links) == 0:
            return ""
        links_html = ""
        for label, url in menu_links:
            links_html += f"""
            <li><a class="dropdown-item" href="{url}">{label}</a></li>
            """

        html = f"""
            <div class="dropdown position-relative">
                <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                    {menu_label}
                </button>
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton1">
                    {links_html}
                </ul>
            </div>
        """
        return html

    def tmpl2(self, site_name, logo_alt_text, home_page_url):

        # links= [
        #     {"name": "Home", "url": home_page_url},
        #     {"name": "Features", "url": "/features"},
        #     {"name": "Pricing", "url": "/pricing", "type": "button"},
        #     {"name": "FAQs", "url": "/faqs"},
        #     {"name": "Dropdown", "links": [
        #         {"name": "Dropdown2", "url": "/dropdown2"},
        #         {"name": "Dropdown3", "url": "/dropdown3"},
        #     ]},
        # ]

        links_html = self.generate_links_html(self.links)
        center_links_html = self.generate_links_html(self.center_links, bold=True, size_em=1.1)

        dropdown_menu_html = self._render_dropdown_links_html(self.drop_down_menu_label, self.drop_down_menu_links)

        navbar_color_style = """style='background-color: #e3f2fd;'"""
        logo_height = "50"
        #dropdown_html = self.dropdown_tmpl("Dropdown", dropdown_links)
        if site_name is None:
            site_name_html = ""
        else:
            site_name_html = f"<span style='font-size: 1.5rem; font-weight: bold;'>{site_name}</span>"
        html = f"""
        <nav class="navbar navbar-expand-sm py-1 mb-4">
            <div class="container-fluid mt-2">
                <a class="navbar-brand d-flex align-items-center" href="{home_page_url}">
                    <img src="{self.logo_src}" alt="{self.logo_alt_text}" height="{logo_height}" class="d-inline-block align-text-top me-5" style="padding-left: 30px;">
                    {site_name_html}
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-end" id="navbarNavDropdown">
                    <ul class="navbar-nav ms-auto">
                        {center_links_html}
                        {links_html}
                    </ul>
                </div>

                {dropdown_menu_html}
            </div>
        </nav>
        """

        style = """
        <style>
        @media (min-width: 576px) {
            .navbar-nav .dropdown-menu {
                position: absolute;
                right: 0;
                left: auto;
            }
        }
        </style>
        """

        html += style


#         html = """
# <nav class="navbar navbar-expand-lg bg-body-tertiary">
#   <div class="container-fluid">
#     <a class="navbar-brand" href="#">Navbar</a>
#     <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
#       <span class="navbar-toggler-icon"></span>
#     </button>
#     <div class="collapse navbar-collapse" id="navbarSupportedContent">
#       <ul class="navbar-nav me-auto mb-2 mb-lg-0">
#         <li class="nav-item">
#           <a class="nav-link active" aria-current="page" href="#">Home</a>
#         </li>
#         <li class="nav-item">
#           <a class="nav-link" href="#">Link</a>
#         </li>
#         <li class="nav-item dropdown">
#           <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
#             Dropdown
#           </a>
#           <ul class="dropdown-menu">
#             <li><a class="dropdown-item" href="#">Action</a></li>
#             <li><a class="dropdown-item" href="#">Another action</a></li>
#             <li><hr class="dropdown-divider"></li>
#             <li><a class="dropdown-item" href="#">Something else here</a></li>
#           </ul>
#         </li>
#         <li class="nav-item">
#           <a class="nav-link disabled" aria-disabled="true">Disabled</a>
#         </li>
#       </ul>
#       <form class="d-flex" role="search">
#         <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
#         <button class="btn btn-outline-success" type="submit">Search</button>
#       </form>
#     </div>
#   </div>
# </nav>
#         """
        return html
    
    def render(self):
        html=self.tmpl2(self.site_name, self.logo_alt_text, self.home_page_url)
        return RenderResponse(html=html)


    def render3(self):
        # Start of the HTML header

        header_classes = "nav d-flex flex-wrap justify-content-center py-3 mb-4"
        # header_classes = "nav col-12 col-md-auto mb-2 justify-content-center mb-md-0"

        logo_site_name = f"""
                    <a href="{self.home_page_url}" class="d-flex align-items-center col-md-3 mb-2 mb-md-0 text-dark text-decoration-none header-site-name">
                <img class="d-block" src="{self.logo_src}" alt="" width="40" style="padding-right: 10px;">
                {self.site_name}
            </a>
        """

        html = f"""
        <header class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between pt-1 pb-1 mb-4" style='background-color: #eaeaff;'>
            <a href="{self.home_page_url}" class="d-flex align-items-center col-md-3 mb-2 mb-md-0 text-dark text-decoration-none header-site-name">
                <img class="d-block" src="{self.logo_src}" alt="" width="{self.logo_height}" style="padding-left: 20px; padding-right: 10px;">
                <span class="fs-4">{self.site_name}</span>
            </a>
            <ul class="{header_classes}">"""

        # Dynamically add each navigation link
        # links_html = '<ul class="nav nav-pills">'
        # for link in self.links:
        #     selected_class = "active" if link["name"] == self.current_item else ""
        #     # links_html += f'<li><a href="{link["url"]}" class="header-link px-2 {selected_class}">{link["name"]}</a></li>'
        #     h = f"""
        #         <li class="nav-item">
        #             <a href="{link["url"]}" class="nav-link {selected_class}" style='color: black;' aria-current="page">
        #                 {link["name"]}
        #             </a>
        #         </li>"""
        #     links_html += h
        # links_html += "</ul>"

        # Close the list of navigation links and add login and sign-up buttons

        # self._add_button("Log In", self.login_url)
        # self._add_button("Sign-Up", self.sign_up_url)
        # self._add_button("Sign-Out", self.sign_out_url)

        # buttons_html = "".join(self.buttons)
        # if self.login_url is not None:
        #     login_button_html = f'''
        #             <button type="button" onclick="window.location.href='{self.login_url}'" class="btn btn-outline-primary me-2 header-login-button">Login</button>
        #     '''
        # else:
        #     login_button_html = ""

        # if self.sign_up_url is not None:
        #     signup_button_html = f'''
        #             <button type="button" onclick="window.location.href='{self.sign_up_url}'" class="btn btn-primary header-signup-button">Sign-Up</button>
        #     '''
        # else:
        #     signup_button_html = ""

        # if self.sign_out_url is not None:
        #     signout_button_html = f'''
        #             <button type="button" onclick="window.location.href='{self.sign_out_url}'" class="btn btn-primary header-signout-button">Sign-Out</button>
        #     '''
        # else:
        #     signout_button_html = ""

        buttons_html = self._render_buttons_html()
        html += f"""
            </ul>
            <div class="col-md-3 text-end">
                {buttons_html}
            </div>
        </header>"""

    #     old_links_html = """
    #           <ul class="nav nav-pills">
    #     <li class="nav-item"><a href="#" class="nav-link active" aria-current="page">Home</a></li>
    #     <li class="nav-item"><a href="#" class="nav-link">Features</a></li>
    #     <li class="nav-item"><a href="#" class="nav-link">Pricing</a></li>
    #     <li class="nav-item"><a href="#" class="nav-link">FAQs</a></li>
    #     <li class="nav-item"><a href="#" class="nav-link">About</a></li>
    #   </ul>
    #   """

        #     html = f'''
        # <header class="d-flex flex-wrap justify-content-center py-3 mb-4">
        #   <a href="{self.home_page_url}" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
        #     <img class="d-block" src="{self.logo_src}" alt="" width="40" style="padding-right: 10px;">
        #     <span class="fs-4">{self.site_name}</span>
        #   </a>

        # {links_html}
        # </header>
        #'''
        return RenderResponse(html=html)

    @staticmethod
    def example(view="default"):
        # Provide an example usage of the HeaderComponent

        site_name = "Example Site"
        logo_src = "/statics/logo.png"
        logo_height = 40
        home_page_url = "/"

        if view == "signin":
            example_links = [
                {"name": "Home", "url": home_page_url},
                # {"name": "Features", "url": "/features"},
                # {"name": "Pricing", "url": "/pricing"},
                # {"name": "FAQs", "url": "/faqs"},
                # {"name": "About", "url": "/about"}
            ]
            example_component = HeaderComponent(
                site_name=site_name,
                logo_src=logo_src,
                logo_height=logo_height,
                home_page_url=home_page_url,
                links=example_links,
                # login_url=None,
                # sign_up_url="/signup",
                # sign_out_url=None,
                # current_item=None,
            )
            return example_component

        if view == "signup":
            example_links = [
                {"name": "Home", "url": home_page_url},
            ]
            example_component = HeaderComponent(
                site_name,
                logo_src,
                logo_height,
                home_page_url,
                links=example_links,
                # login_url="/signin",
                # sign_up_url=None,
                # sign_out_url=None,
                # current_item=None,
            )
            return example_component

        example_links = [
            {"name": "Home", "url": home_page_url},
            {"name": "Features", "url": "/features"},
            {"name": "Pricing", "url": "/pricing"},
            {"name": "FAQs", "url": "/faqs"},
            {"name": "About", "url": "/about"},
        ]
        example_component = HeaderComponent(
            site_name="Example Site",
            logo_src="/statics/logo.png",
            logo_height=logo_height,
            home_page_url=home_page_url,
            links=example_links
        )
        return example_component

