

import os
from flask import (url_for)
from uilib.components import DyGraphChart


class PageBuilder:

    def __init__(self, title):
        self.title = title
        self.modules_html = []
        self.modules_js = []

    def add_module_raw(self, html, js=None):
        self.modules_html.append(html)
        if js is not None:
            self.modules_js.append(js)

    # def get_module(self, name, attrs):
    #
    #     if name == 'monitors':
    #         dataset_id = attrs.get('dataset', None)
    #         if dataset_id is not None:
    #             (df_html, df_js) = render_monitors_table([dataset_id])
    #             return (df_html, df_js)
    #
    #     if name == 'tabs_dataset':
    #         dataset_id = attrs.get('dataset', None)
    #         views = attrs.get('views', [])
    #         selected_view = attrs.get('selected', None)
    #         html = render_dataset_page_tabs(dataset_id, views, selected_view)
    #         html = "<p class='table_title'>Data</p><br>" + html
    #         return (html, '')
    #
    #     if name == 'page_header':
    #         category = attrs.get('category', None)
    #         name = attrs.get('name', None)
    #         mattrs = attrs.get('attrs', None)
    #         html = render_page_header(category, name, mattrs)
    #         return (html, '')
    #
    #     if name == 'dataset':
    #         dataset = attrs.get('dataset_obj', None)
    #         view = attrs.get('view', None)
    #         table_css_idx = attrs.get('table_idx', None)
    #         df = dataset.get_dataset_view(view=view, skip_cache=False)
    #         (df, msg) = truncate_df(df, row_limit=500)
    #         df = df.reset_index()
    #         title = None
    #         (df_html, df_js) = render_df(title, df, css_id="tbl%d" % table_css_idx, show_index=False)
    #         return (msg + df_html, df_js)
    #
    #     if name == 'dashboards_table':
    #         dataset_id = attrs.get('dataset', None)
    #         (html, js) = render_dashboards_table(dataset_id)
    #         return (html, js)
    #
    #     if name == 'plot_metrics':
    #         dataset = attrs.get('dataset_obj', None)
    #         df = dataset.get_dataset_view(view="metrics", skip_cache=True)
    #         (graphs_html, graphs_js) = render_multiple_graphs(dataset.id, df)
    #         return (graphs_html, graphs_js)
    #
    #     ('', '')


    def _render_df_chart(self, graph_idx, title, data_url, checkboxes=None):
        graph = DyGraphChart()
        (chart_html, footer_scripts) = graph.render(title, data_url, css_id="graph%d" % graph_idx, checkboxes=checkboxes)
        # head_scripts = DyGraphChart.get_head_scripts()
        return (chart_html, footer_scripts)


    def add_module_by_name(self, name, attrs):
        (html, js) = self.get_module(name, attrs)
        self.add_module_raw(html, js)

    def render_modules(self):
        html = "<br>\n".join(self.modules_html)
        js = "\n".join(self.modules_js)
        return (html, js)

    def _get_page_attrs(self, body, head_scripts, footer_scripts, css_links):
        default_page_attrs = {
            "TITLE": "Title",
            "SITE_NAME": "amelie",
            "NAV_ITEM1": "",  # '<li><a href="%s">Search</a></li>' % url_for("search_results"),
            "NAV_ITEM2": "",
            "NAV_ITEM3": "",
            "HOME_URL": "", #url_for("home"),
            "HEAD_SCRIPTS": head_scripts,
            "CSS_LINKS": css_links,
            "BODY": body,
            "ALERT": "",
            "READY_JS": "",
            "FOOTER_SCRIPTS": footer_scripts,
        }
        return default_page_attrs

    def _render_tmpl(self, template_dir, fn, attrs):
        fn = os.path.join(template_dir, fn)
        if not os.path.exists(fn):
            print("ERROR: render_tmpl(), path %s does not exist" % fn)
            return ""
        with open(fn, "r") as f:
            html = f.read().replace("\n", "")
            for key in attrs.keys():
                value = attrs[key]
                tkey = "{%s}" % key
                html = html.replace(tkey, value)
        return html

    def render_page(self):

        statics_base_dir = '/packages/uilib/uilib/statics/'
        templates_dir = statics_base_dir + "/templates"
        default_page_tmpl = "bootstrap_page.html"

        (modules_html, modules_js) = self.render_modules()
        body = modules_html
        footer_scripts = modules_js
        head_scripts = ''

        css_url = url_for("statics_page.static_file", file='style.css')
        css_links = "<link rel='stylesheet' type='text/css' href='%s'>" % css_url
        return self._render_tmpl(
            templates_dir,
            default_page_tmpl,
            self._get_page_attrs(body, head_scripts=head_scripts, footer_scripts=footer_scripts, css_links=css_links),
        )
