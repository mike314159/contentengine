import decimal
import os
#from flask_wtf import FlaskForm
#from wtforms import Form, BooleanField, StringField, DateTimeField, TextAreaField, DecimalField, SelectField, validators
from flask import url_for, make_response
from uilib.renderresponse import RenderResponse




class PageBuilder():

    def __init__(self, page_title='Untitled Page', page_template='bootstrap_page.html', canonical_url=None, 
        statics_base_dir=None, meta_description=None, meta_properties=None):

        if statics_base_dir is None:
            self.statics_base_dir = '/packages/uilib/uilib/statics/'
        else:
            self.statics_base_dir = statics_base_dir

        self.page_title = page_title
        self.meta_description = meta_description
        self.meta_properties = meta_properties
        self.canonical_url = canonical_url
        self.css_id = 0
        self.page_template = page_template
        self.body_components = []
        self.header_component = None
        self.footer_components = []
        self.header_js = []
        self.other_links = ''

    def next_css_id(self):
        self.css_id += 1
        return "comp%d" % self.css_id
    
    def add_header_js(self, header_js):
        self.header_js.append(header_js)

    def add(self, component, position=None):
        if component is None:
            return
        if position is not None:
            if position == 'header':
                self.header_component = component
            elif position == 'footer':
                self.footer_components.append(component)
            elif position == 'body':
                self.body_components.append(component)
        else:
            self.body_components.append(component)

    def add_favicon(self, favicon_url):
        self.other_links += '<link rel="icon" type="image/x-icon" href="%s">' % favicon_url

    # def _get_page_attrs(self, body, head_scripts, footer_scripts, css_links):

        # attrs = {
        #     'PAGE_TITLE': self.page_title,
        #     'HEAD_SCRIPTS': self.head_scripts,
        #     'FOOTER_SCRIPTS': self.footer_scripts,
        #     #'CSS_LINKS': css_links,
        #     'BODY': body,
        # }
    #     {CSS_LINKS}
    #     {HEAD_SCRIPTS}
    #     {BODY}
    #     {FOOTER_SCRIPTS}
    #     '''

    #     default_page_attrs = {
    #         "PAGE_TITLE": self.page_title,
    #         "SITE_TITLE": self.site_title,
    #         "NAV_ITEM1": "",  # '<li><a href="%s">Search</a></li>' % url_for("search_results"),
    #         "NAV_ITEM2": "",
    #         "NAV_ITEM3": "",
    #         "HOME_URL": self.home_url,
    #         "HEAD_SCRIPTS": head_scripts,
    #         "CSS_LINKS": css_links,
    #         "BODY": body,
    #         "ALERT": "",
    #         "READY_JS": "",
    #         "FOOTER_SCRIPTS": footer_scripts,
    #     }
    #     return default_page_attrs

    def _render_tmpl(self, template_dir, fn, attrs):
        fn = os.path.join(template_dir, fn)
        if not os.path.exists(fn):
            print("ERROR: render_tmpl(), path %s does not exist" % fn)
            return ""
        with open(fn, "r") as f:
            html = f.read().replace("\n", "")
            for key in attrs.keys():
                value = attrs[key]
                if value is None:
                    value = ""
                tkey = "{%s}" % key
                html = html.replace(tkey, value)
        return html

    def render_body_components(self):
        resp = RenderResponse()
        for c in self.body_components:
            if c is None:
                continue
            cresp = c.render()
            resp.add_response(cresp)
        return resp

    def render(self, status_code=None):

        templates_dir = self.statics_base_dir + "/templates"

        resp = RenderResponse()

        css_url = url_for("statics_page.static_file", file='style.css')
        css_links = "<link rel='stylesheet' type='text/css' href='%s'>" % css_url
        resp.add_css_links(css_links)

        bresp = self.render_body_components()
        resp.add_response(bresp)

        body_html = resp.get_html()
        head_scripts = resp.get_header_js()
        footer_js = resp.get_footer_js()
        css_links = resp.get_css_links()

        addl_head_js = "\n".join(self.header_js)
        head_scripts = head_scripts + addl_head_js

        if self.header_component is not None:
            header_html = self.header_component.render().get_html()
        else:
            header_html = ""
        if len(self.footer_components) > 0:
            footer_html = ""
            for c in self.footer_components:
                footer_html += c.render().get_html()
        else:
            footer_html = ""

        attrs = {
            'PAGE_TITLE': self.page_title,
            'HEAD_SCRIPTS': head_scripts,
            'FOOTER_SCRIPTS': footer_js,
            'OTHER_LINKS': self.other_links,
            'CSS_LINKS': css_links,
            'HEADER': header_html,
            'BODY': body_html,
            'FOOTER': footer_html,
        }

        if self.canonical_url is not None:
            s = '\n<link rel="canonical" href="%s">' % self.canonical_url
            attrs['CANONICAL_URL'] = s
        else:
            attrs['CANONICAL_URL'] = ""

        if self.meta_description is not None:
            s = '\n<meta name="description" content="%s">' % self.meta_description
            attrs['META_DESCRIPTION'] = s
        else:
            attrs['META_DESCRIPTION'] = ""

        if self.meta_properties is not None:
            s = [""]
            for key, value in self.meta_properties.items():
                s.append('<meta property="%s" content="%s">' % (key, value))
            attrs['META_PROPERTIES'] = "\n".join(s)
        else:
            attrs['META_PROPERTIES'] = ""

        page_html = self._render_tmpl(
            templates_dir,
            self.page_template,
            attrs
        )
    
        if status_code is not None:
            response = make_response(page_html)
            response.status_code = status_code
            return response
        else:
            response = make_response(page_html)
            #response.headers['X-Custom-Header'] = 'My custom header'
            #response.set_cookie('my_cookie', 'value')
            return response

