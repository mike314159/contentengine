import random
import os
import socket
import json
import urllib
import ast

from uilib.renderresponse import *
from uilib import renderhelpers as rh
from uilib.components import dygraphchart as dg
from uilib.components import autocomplete as ac
from uilib.dftemplate import DFTemplate
#from uilib.formbuilder import *
from uilib.components import BillboardChart

from uilib.pagebuilder import *
from uilib.basecomponents import *
from uilib.components import *
from uilib.components import SignUpFormComponent
from uilib.components import LoginFormComponent
from uilib.components import PasswordResetFormComponent


def get_all_component_classes():
    """
    Returns a list of tuples containing (class_name, filename) for all classes in the components subdirectory
    that derive from the Component class.
    
    Returns:
        list: List of tuples where each tuple is (class_name, filename)
    """
    components_dir = os.path.join(os.path.dirname(__file__), 'components')
    class_tuples = []
    
    if not os.path.exists(components_dir):
        return []
    
    # Get all Python files in the components directory
    for filename in sorted(os.listdir(components_dir)):
        if filename.endswith('.py') and filename != '__init__.py':
            file_path = os.path.join(components_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Use regex to find class definitions that inherit from Component
                import re
                # Pattern to match: class ClassName(Component): or class ClassName(Component):
                pattern = r'class\s+(\w+)\s*\(\s*Component\s*\)\s*:'
                matches = re.findall(pattern, content)
                
                for class_name in matches:
                    class_tuples.append((class_name, filename))
                        
            except Exception as e:
                print(f"Error parsing {file_path}: {e}")
                continue
    
    return class_tuples


from uilib.components import FormConfirmationComponent
#from uilib.usereditformcomponent import UserEditFormComponent
from uilib.components import BillboardBarChart
from uilib.components import HeaderComponent
from uilib.components import VerticalFormComponent
from uilib.components import CarouselComponent

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    send_from_directory,
    url_for,
    make_response,
    Response,
    current_app,
)

import pandas as pd
import datetime
import random
import time

statics_base_dir = '/packages/uilib/uilib/statics/'
templates_dir = statics_base_dir + "/templates"
default_page_tmpl = "bootstrap_page.html"

#from flask_wtf import FlaskForm
#from wtforms import Form, BooleanField, StringField, DateTimeField, TextAreaField, DecimalField, SelectField, validators

from flask import Flask, render_template_string

#
# from __main__ import app
#
#
#

def get_page_attrs(body, footer_scripts, css_links='', head_scripts=''):
    return {
        "TITLE": "Tests Page",
        # "SITE_NAME": "Site Name",
        # "NAV_ITEM1": '',
        # "NAV_ITEM2": '',
        # "NAV_ITEM3": '',
        # "HOME_URL": "/",
        "HEAD_SCRIPTS": head_scripts,
        "CSS_LINKS": css_links,
        "BODY": body,
        # "ALERT": "",
        # "READY_JS": "",
        "FOOTER_SCRIPTS": footer_scripts,
    }


from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

uilib_tests_blp = Blueprint('uilib_tests', __name__)


from flask import current_app, url_for

def list_routes(blueprint):
    urls = []
    for rule in current_app.url_map.iter_rules():
        if rule.endpoint.startswith(blueprint.name):
            options = {}
            for arg in rule.arguments:
                options[arg] = f"[{arg}]"
            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint, **options)
            line = f"{rule.endpoint:50s} {methods:20s} {url}"
            urls.append(url)
    
    return urls

# Usage:
# routes_list = list_routes(uilib_tests_blp)


@uilib_tests_blp.route('/')
def tests_home_page():
    rnum = random.randint(1, 100)


    routes_list = list_routes(uilib_tests_blp)
    print(routes_list)

    htmls = []

    htmls.append(f"<h3>UI Lib Tests Page</h3>")
    
    parsed_url = urllib.parse.urlparse(request.base_url)
    hostname = parsed_url.hostname
    htmls.append(f"<b>URL Parse Hostname:</b> {hostname}")

    hostname=socket.gethostname()
    htmls.append(f"<b>Socket gethostname:</b> {hostname}") 
    htmls.append(f"<b>Random:</b> {rnum}")

    # for url in routes_list:
    #     htmls.append(f"<br><a href='{url}'>{url}</a>")



    routes = [
        "uilib_tests.direct_image_serve_page",
        "uilib_tests.test_data_csv_page",
    ]

    htmls.append(f"<br><b>Direct Serving Routes:</b>")
    for url in routes:
        htmls.append(f"<br><a href='{url_for(url)}'>{url}</a>")

    routes = [
        "uilib_tests.blank_page_render_page",
        "uilib_tests.basic_page_render",
    ]

    htmls.append(f"<br><b>Page Render Routes:</b>")
    for url in routes:
        htmls.append(f"<br><a href='{url_for(url)}'>{url}</a>")

    htmls.append(f"<br><b>Component Routes:</b>")
    #routes = []


    # Add component classes information
    # htmls.append(f"<br><br><b>Component Classes:</b>")
    class_tuples = get_all_component_classes()
    # htmls.append(f"<br>Total classes found: {len(class_tuples)}")
    # htmls.append(f"<br><br><b>All Component Classes (Class Name, Filename):</b>")
    
    for class_name, filename in class_tuples:
        url = url_for("uilib_tests.render_component_page") + "?class=" + class_name
        #routes.append(url)
        htmls.append(f"<a href='{url}'>{class_name}</a>")

    # for url in routes:
    #     htmls.append(f"<br><a href='{url_for(url)}'>{url}</a>")

    return "<br>".join(htmls)


def render_page(body_components):

    # header = HeaderComponent.example()

    # links = [
    #     {"name": "Home", "url": "/"},
    #     {"name": "Privacy Policy", "url": "/privacy-policy"},
    #     {"name": "About", "url": "/about"}
    # ]
    # site_name = "Sample Site Name"
    # footer = SimpleFooterComponent(site_name, links)

    container_body = Container(cols=1, components=body_components)

    site_config = current_app.config['SITE_CONFIG']
    ui_lib_statics_base_dir = site_config.get_uilib_statics_base_dir()

    pb = PageBuilder(page_title="No Page Title", page_template="bootstrap_empty.html", statics_base_dir=ui_lib_statics_base_dir)

    # pb.add(header, position="header")
    # pb.add(footer, position="footer")
    pb.add(container_body, position="body")

    return pb.render()



# Directly serve an image
@uilib_tests_blp.route("/direct_image_serve")
def direct_image_serve_page():
    test_imgs_dir = os.path.join(statics_base_dir, "images")
    return send_from_directory(test_imgs_dir, "test.jpeg")

# Test Render a Page
@uilib_tests_blp.route("/blank-page")
def blank_page_render_page():
    pb = PageBuilder(page_title='Blank Page', page_template='bootstrap_empty.html')
    pb.add(HTMLComponent(html='<p>Blank Page Render</p>'))
    return pb.render()

@uilib_tests_blp.route("/basic-page-render")
def basic_page_render():
    return render_page([HTMLComponent(html='<p>Basic Page Render</p>')])


@uilib_tests_blp.route("/component")
def render_component_page():
    component_class_name = request.args.get('class')
    component = globals()[component_class_name].example()
    return render_page([component])


@uilib_tests_blp.route("/components")
def render_all_components_page():
    """
    Renders all available components on a single page for testing and demonstration.
    Each component is wrapped in a section with its name as a heading.
    """
    all_components = []
    failed_components = []
    
    # Get all component classes
    component_classes = get_all_component_classes()
    
    for class_name, filename in component_classes:

        try:
            # Create a heading for each component
            html = "<hr>"
            html += f"<span style='color: #cc0000; font-weight: 500;'>Rendering: <a href='/tests/component?class={class_name}' target='_blank' style='color: #cc0000;'>{class_name}</a></span>"

            all_components.append(HTMLComponent(html=html))

            #heading = TextHeading(text=f"{class_name} ({filename})", level=2)
            #all_components.append(heading)
            
            # Add a separator line
            #separator = LineBreak()
            #all_components.append(separator)
            
            # Create the component instance using its example method

            #if class_name in globals():
            component = globals()[class_name].example()
            all_components.append(component)


            all_components.append(HTMLComponent(html='done'))

            # else:
            #     html = f"Component {class_name} not found"
            #     all_components.append(html)
            
            # Add some spacing between components
            # spacing = LineBreak()
            # all_components.append(spacing)
            # spacing2 = LineBreak()
            # all_components.append(spacing2)
            
        except Exception as e:
            # If a component fails to load, add an error message
            html = f"Error rendering {class_name}: {str(e)}"
            all_components.append(HTMLComponent(html=html))
            failed_components.append(class_name)
            # all_components.append(html)
            # all_components.append(error_heading)
            # error_separator = LineBreak()
            # all_components.append(error_separator)
    
    # Add a section at the bottom listing all failed components
    if failed_components:
        all_components.append(HTMLComponent(html="<hr><h3>Components that are not working:</h3>"))
        for component_name in failed_components:
            all_components.append(HTMLComponent(html=f"{component_name}"))
    
    return render_page(all_components)



# @uilib_tests_blp.route("/hero_component")
# def hero_component():
#     return render_page([HeroComponent.example()])


# @uilib_tests_blp.route("/pricing_component")
# def pricing_component():
#     return render_page([PricingPlansComponent.example()])


# @uilib_tests_blp.route("/features_component")
# def features_component():
#     return render_page([FeaturesComponent.example()])

# @uilib_tests_blp.route("/vertical_form_signin_example")
# def vertical_form_signin_example():
#     comp = VerticalFormComponent.example(view="signin")
#     return render_page([comp])

# @uilib_tests_blp.route("/vertical_form_signup_example")
# def vertical_form_signup_example():
#     comp = VerticalFormComponent.example(view="signup")
#     return render_page([comp])

# @uilib_tests_blp.route("/vertical_form_password_reset_example")
# def vertical_form_password_reset_example():
#     comp = VerticalFormComponent.example(view="password-reset")
#     return render_page([comp])

# @uilib_tests_blp.route("/login_form_component")
# def login_form_component():
#     comp = LoginFormComponent.example()
#     return render_page([comp])

# @uilib_tests_blp.route("/sign_up_component")
# def sign_up_component():
#     comp = SignUpFormComponent.example()
#     return render_page([comp])

# @uilib_tests_blp.route("/password_reset_component")
# def password_reset_component():
#     comp = PasswordResetFormComponent.example()
#     return render_page([comp])

# @uilib_tests_blp.route("/form_confirmation_components")
# def form_confirmation_components():
#     signup_success = FormConfirmationComponent.example(view='signup_success')
#     hr_comp = HTMLComponent(html="<hr>")
#     signup_failure = FormConfirmationComponent.example(view='signup_failure')
#     return render_page([comp1, hr_comp, comp2])

# @uilib_tests_blp.route("/all_auth_components")
# def all_auth_components():
#     login_comp = LoginFormComponent.example()
#     signup_comp = SignUpFormComponent.example()
#     signup_success = FormConfirmationComponent.example(view='signup_success')
#     signup_failure = FormConfirmationComponent.example(view='signup_failure')
#     password_reset_comp = PasswordResetFormComponent.example()
#     hr_comp = HTMLComponent(html="<hr>")
#     return render_page([login_comp, hr_comp, signup_comp, hr_comp, signup_success, hr_comp, signup_failure, hr_comp, password_reset_comp])

# @uilib_tests_blp.route("/carousel_component")
# def carousel_component():
#     comp = CarouselComponent.example()
#     return render_page([comp])

# @uilib_tests_blp.route("/user_edit_component")
# def user_edit_component():
#     comp = UserEditFormComponent.example()
#     return render_page([comp])



# @uilib_tests_blp.route("/sample-signin-page")
# def sample_signin_page():
#     pb = PageBuilder(page_template="bootstrap_empty.html")

#     header = HeaderComponent.example(view="signin")
#     pb.add(header, position='header')

#     signin = VerticalFormComponent.example(view="signin")
#     pb.add(signin)

#     return pb.render()


# @uilib_tests_blp.route("/sample-signup-page")
# def sample_signup_page():
#     pb = PageBuilder(page_template="bootstrap_empty.html")

#     header = HeaderComponent.example(view="signup")
#     pb.add(header)

#     signup = VerticalFormComponent.example(view="signup")
#     pb.add(signup)

#     return pb.render()

# @uilib_tests_blp.route("/sample-password-reset-page")
# def sample_password_reset_page():
#     pb = PageBuilder(page_template="bootstrap_empty.html")

#     header = HeaderComponent.example(view="signin")
#     pb.add(header)

#     reset = VerticalFormComponent.example(view="password-reset")
#     pb.add(reset)

#     return pb.render()

# @uilib_tests_blp.route("/sample-form-confirmation")
# def sample_form_confirmation_page():

#     pb = PageBuilder(page_template="bootstrap_empty.html")

#     header = HeaderComponent.example()
#     pb.add(header)

#     comp = FormConfirmationComponent.example()
#     pb.add(comp)

#     return pb.render()










# @uilib_tests_blp.route("/test-grid-component-render")
# def test_grid_component_page():

#     pb = PageBuilder()

#     grid = GridComponent()
#     grid.add_cell('Column 1')
#     grid.add_cell('Column 2')
#     grid.add_cell('Column 3')
#     grid.add_cell('Column 4')
#     grid.add_cell('Column 5')
#     pb.add(grid)
    
#     return pb.render()


# @uilib_tests_blp.route("/test-modal")
# def test_modal_page():
#     pb = PageBuilder()
#     comp = ModalComponent()
#     pb.add(comp)
#     return pb.render()



# @uilib_tests_blp.route("/test-df-render")
# def test_df_render_page():

#     df = get_random_df()

#     pb = PageBuilder()
#     #cont = Container(cols=1)
#     #pb.add_container(cont)

#     css_id = "tbl1" 
#     comp = DataframeTable(df, css_id, show_index=False)
#     pb.add(comp)

#     return pb.render()


    # #(html, js) = rh.render_df("Test DF Render", df, css_id="tbl1", show_index=False)

    # #(html, js) = DFTemplate.format_and_render(title="Test DF Render", df=df, cols=None, css_id="tbl1", show_search=True)

    # title = "Test DF Render"
    # css_id = "tbl1"

    # #(html, js) = DFTemplate.render_df(title, df, css_id, show_index=True, show_search=True)

    # tmpl = DFTemplate()
    # (html, js) = tmpl.render(
    #         df=df, css_id=css_id, title=None, show_search=True, show_index=True, striped=True, cell_class_fmts=None,
    #         cell_value_fmts=None, link_fmts=None
    # )


    # title = "Test Page"

    # head_scripts = ""
    # return rh.render_tmpl(
    #     templates_dir,
    #     default_page_tmpl,
    #     get_page_attrs(html, footer_scripts=js)
    # )

# Show an example graph from the dygraph library
@uilib_tests_blp.route("/test-data-csv")
def test_data_csv_page():
    csv = "Date, High, Low, Close\n"
    dt = datetime.date(2018, 1, 1)
    a = random.randint(1, 300)
    b = random.randint(1, 100)
    c = random.randint(1, 50)
    for i in range(1, 200):
        a += random.randint(-10, 10)
        b += random.randint(-10, 10)
        c += random.randint(-10, 10)
        csv += "%s,%d,%d,%d\n" % (
            dt.strftime("%Y%m%d"),
            a,
            b,
            c,
        )
        dt += datetime.timedelta(days=1)

    #response = app.response_class(response=csv, status=200, mimetype="application/text")
    response = Response(csv, status=200, mimetype="text/csv")
    return response

# @uilib_tests_blp.route("/test-dygraphs")
# def test_dygraphs_page():

#     graph = dg.DyGraphChart()
#     css_links = dg.DyGraphChart.get_css_links()
#     head_scripts = dg.DyGraphChart.get_head_scripts()

#     # data_url1 = "/static/dygraph/temperatures.csv"
#     # (chart_html1, footer_scripts1) = graph.render(data_url1, css_id='graph1')
#     data_url2 = url_for("uilib_tests.test_data_csv_page")
#     title = "Test Graph"
#     (chart_html2, footer_scripts2) = graph.render(title, data_url2, css_id="graph2")

#     body_html = chart_html2
#     footer_js = footer_scripts2
#     html = rh.render_tmpl(
#         templates_dir,
#         default_page_tmpl,
#         get_page_attrs(body_html, footer_scripts=footer_js) #, css_links=css_links),
#     )
#     return html

# @uilib_tests_blp.route("/test-billboard-line-chart")
# def test_billboard_line_chart_page():

#     pb = PageBuilder()
   
#     df = get_random_df(length=200)
    
#     comp = TimeseriesChart(df, chart_num=1, y_columns=list(df.columns), y_axis_label='This is the Y Label', x_column=None)
#     pb.add(comp)

#     return pb.render()

# @uilib_tests_blp.route("/test-billboard-bar-chart")
# def test_billboard_bar_chart_page():

#     pb = PageBuilder()
   
#     df = pd.DataFrame()
#     now_dt = datetime.datetime.now()
#     for i in range(6,0,-1):
#         dt = now_dt - datetime.timedelta(days=i)
#         dt_str = dt.strftime("%Y-%m-%d")
#         df.at[dt_str, 'data1'] = i

#     comp = BillboardBarChart(chart_num=1, df=df, columns=list(df.columns), y_axis_label='This is the Y Label', show_legend=True, height='600px')
#     pb.add(comp)

#     return pb.render()



@uilib_tests_blp.route("/random-chart-data")
def random_chart_data_page():

    num_lines = int(request.args.get('num_lines', 2))

    min_value = int(request.args.get('min', 0))
    max_value = int(request.args.get('max', 100))
    #format = request.args.get('format', 'csv')

    # data = []
    # for i in range(1, 100):
    #     data.append(random.randint(1, 100))
    # result = jsonify(data)
    # print(result)
    # return "Hey there!"

    csv = True
    '''
            x,data1,data2
        2013-01-01,30,130
        2013-01-02,200,340
        2013-01-03,100,200
        2013-01-04,400,500
        2013-01-05,150,250
        2013-01-06,250,350
    ''' 

    df = get_random_df(length=20, num_cols=num_lines, min_value=min_value, max_value=max_value)
    #df = get_random_df(length=20)

    format = 'csv'
    if format == 'csv':
        df.index.name = 'x'
        csv = df.to_csv(index=True)
        #print("CSV\n", csv)
        response = Response(csv, status=200, mimetype="application/text")
        return response
    # else:
    #     df = df['value1']
    #     #csv = ",".join(df.astype(str).tolist())
    #     y_values = []
    #     y_values.append('value1')
    #     y_values.extend(df.astype(str).tolist())
    #     #print("Values = ", values)

    #     x_values = ['x']
    #     x_values.extend(df.index.astype(str).tolist())

    #     dct = {
    #         'columns': [
    #             x_values,
    #             y_values
    #         ]
    #     }
    #     j = json.dumps(dct, indent=4)
    #     #print(j)
    #     response = Response(j, status=200, mimetype="application/json")
    #     return response



# @uilib_tests_blp.route("/test-timeseries-swap-line-chart")
# def test_timeseries_swap_line_chart_page():

#     pb = PageBuilder()
   
#     df = get_random_df(length=200)

#     css_id = 'chart1'
#     comp = TimeseriesChart(df, css_id, y_columns=list(['value1']), y_axis_label='This is the Y Label', x_column=None, 
#                            title="Graph Title", sub_title="Graph Subtitle")
#     pb.add(comp)

#     df = get_random_df(length=200)
#     df = df['value1']
#     print(df.head())
#     csv = ",".join(df.astype(str).tolist())
#     print("CSV = ", csv)

#     # convert column value1 in df to a csv string
#     #csv = df.to_csv(index=False)
#     #print("CSV = ", csv)

#     html = '''
#     <button onclick="updateData()">Update Data2</button>
#     '''
#     js = '''
#     <script>
#     function updateData() {
#       chart.load({
#         columns: [
#           ["value1", %s] // new data for data2 series
#         ]
#       });
#     }
#     </script>
#     ''' % csv

#     url = url_for("uilib_tests.random_chart_data_page")
#     js = '''
#     <script>
#         function updateData() {
#             fetch('%s')
#                 .then(response => response.json())
#                 .then(data => {
#                 // Assuming the data from the URL is in the correct format
#                 chart.load({
#                     columns: data.columns
#                 });
#             })
#             .catch(error => console.error('Error fetching data:', error));
#         }
#     </script>
#     ''' % url
#     comp = HTMLComponent(html = html, footer_js=js)
#     pb.add(comp)

#     return pb.render()


# @uilib_tests_blp.route("/test-multi-panel-timeseries-line-chart")
# def test_multi_panel_timeseries_line_chart_page():

#     pb = PageBuilder()
   
#     panel_choices = [
#         ('hi', url_for("uilib_tests.random_chart_data_page", min=100, max=125, format='csv')),
#         ('med', url_for("uilib_tests.random_chart_data_page", min=50, max=75, format='csv')),
#         ('low', url_for("uilib_tests.random_chart_data_page", min=-50, max=-25, format='csv')),
#     ]

#     height = '300px'

#     initial_panel = 'low'
#     chart_num = 1
#     comp = MultiPanelTimeseriesChart(
#         chart_num, panel_choices, initial_panel, 
#         title="Graph Title 1", sub_title="Graph Subtitle", 
#         y_axis_label='This is the Y Label',
#         height=height)
#     pb.add(comp)

#     initial_panel = 'med'
#     chart_num = 2
#     comp = MultiPanelTimeseriesChart(
#         chart_num, panel_choices, initial_panel, 
#         title="Graph Title 2", sub_title="Graph Subtitle", 
#         y_axis_label='This is the Y Label',
#         height=height)
#     pb.add(comp)

#     return pb.render()


# def build_form():
#
#     class AlertForm(FlaskForm):
#         cls = "form-control"
#         above_value = StringField('This is a StringField', [validators.Length(min=0, max=10)])
#         below_value = StringField('This is a StringField', [validators.Length(min=0, max=10)])
#         pct_change = StringField('This is a StringField', [validators.Length(min=0, max=5)])
#         birthday = DateTimeField('This is a DateTimeField', format='%m/%d/%y')
#         signature = TextAreaField('This is a TextAreaField')
#
#     form = AlertForm()
#
#     rows = [
#             [
#                 "Value is above",
#                 {'id': 'above', 'wtf': form.above_value(class_="form-control")},
#                 "or below",
#                 {'id': 'below', 'wtf': form.below_value(class_="form-control")}
#             ],
#             [
#                 "Changes more than",
#                 {'id': 'above', 'wtf': form.pct_change(class_="form-control")},
#                 "percent"
#             ]
#     ]
#     h = ''
#     for row in rows:
#         h += "<div>"
#         for field in row:
#             h += "<div class='row'>"
#             if type(field) == str:
#                 h += "<label for='inputPassword6' class='col-form-label'>%s</label>" % field
#             else:
#                 id = field.get('id')
#                 control = field.get('wtf')
#                 h += str(control)
#             h += "</div>"
#         h += "</div>"
#     return h
#
#
#
#
#



#
# @uilib_tests_blp.route("/test-wtforms", methods=['GET', 'POST'])
# def test_wtforms():
#
#     class MyForm(FlaskForm):
#         cls = "form-control"
#         username = StringField('This is a StringField', [validators.Length(min=4, max=25)])
#         accept_rules = BooleanField('This is a BooleanField', [validators.InputRequired()])
#         birthday = DateTimeField('This is a DateTimeField', format='%m/%d/%y')
#         signature = TextAreaField('This is a TextAreaField')
#
#     post_url = url_for("uilib_tests.test_wtforms")
#     form = MyForm()
#
#     body2 = "<form method='POST' action='%s'>" % post_url
#     for field, info in form.data.items():
#         # body2 += "%s<br>" % field
#         body2 += "%s<br>%s" % (form[field].label, form[field](class_="form-control"))
#         body2 += "<br>"
#     body2 += "<input type='submit' value='Go'>"
#     body2 += "</form>"

#
#
    # fb = FormBuilder()
    # f = fb.get_decimal_field(id=3, value='123')
    #
    # label='Teast Select'
    # choices = [('weekly', 'Weekly'), ('daily', 'Daily'), ('none', 'None')]
    # selected = 'daily'
    # id = 4
    # s = fb.get_select_field(id, label, choices, selected)
    #
    # body5 = f + "<br>" + s
#
# <div>
#     <h3>Price Alert</h3>
#     <p>Get notified when a coin crosses above or below a price target.</p>
#     <label class="col-form-label" style='display: inline'>Above</label>
#     <input type="text" class="form-control" style='display: inline; width: 15%' placeholder="">
#     <label class="col-form-label" style='display: inline'>Below</label>
#     <input type="text" class="form-control" style='display: inline; width: 15%' placeholder="">
# </div>
# <br>
# <div>
#     <h3>Percentage Price Alert</h3>
#     <p>Get notified when a coin changes in value by a specific percent.</p>
#     <label class="col-form-label" style='display: inline'>Changes by</label>
#     <input type="text" class="form-control" style='display: inline; width: 10%' placeholder="">
#     <label class="col-form-label" style='display: inline'>%</label>
# </div>
# <br>
# <div>
#     <h3>Periodic Update</h3>
#     <p>Get notified of the price of an asset at regular intervals. Does not affect alert frequency. Alerts happen daily regardless of this setting.</p>
#     <label class="col-form-label" style='display: inline'>Send status updates</label>
#         <select class="form-select w-25" style='display: inline'>
#           <option value="1">Weekly</option>
#           <option value="2">Daily</option>
#           <option value="3">Never</option>
#         </select>
# </div>
#     '''
#    body = body2 + "<br><br>"

    # if request.method == 'GET':
    #     html = '''
    #         <form method="POST" action="%s">
    #             {{ form.csrf_token }}
    #             <br><br>{{ form.username.label }} {{ form.username(size=20) }}
    #             <br><br>{{ form.accept_rules.label }} {{ form.accept_rules }}
    #             <br><br>{{ form.birthday.label }} {{ form.birthday }}
    #             <br><br>{{ form.signature.label }}{{ form.signature }}
    #             <br><br><input type="submit" value="Go">
    #         </form>
    #     ''' % post_url
    #     body1 = render_template_string(html, form=form)
    #
    #
    #
    #     body = body1 + "<br><br>" + body2
    #
    # if request.method == 'POST':
    #     if form.validate_on_submit():
    #         #return redirect('/success')
    #         body = 'Success'
    #     else:
    #         print(form.data)
    #         html = '''
    #             {% for field, errors in form.errors.items() %}
    #             <div class="alert alert-error">
    #                 {{ form[field].label }}: {{ ', '.join(errors) }}
    #             </div>
    #             {% endfor %}
    #         '''
    #         body = 'Validation Failed<br>'
    #         body += render_template_string(html, form=form)
    #     #return render_template('submit.html', form=form)

    # return rh.render_tmpl(
    #     templates_dir,
    #     default_page_tmpl,
    #     get_page_attrs(body, footer_scripts="")
    # )

# @uilib_tests_blp.route("/test-form-builder", methods=['GET', 'POST'])
# def test_form_builder():

#     #--------------------------

#     fb = FormBuilder(request)
#     fb.add_text_field('search')

#     fb.add_section(
#         'Search',
#         'Enter one or more asset names or symbols separated by commas.',
#         [
#             (FormBuilder.CONTROL, 'search')
#         ]
#     )

#     post_url = url_for("uilib_tests.test_form_builder")
#     body1 = fb.render(post_url)

#     #--------------------------

#     fr = FormBuilder(request)
#     fr.add_decimal_field('above_value')
#     fr.add_decimal_field('below_value')
#     fr.add_decimal_field('pct_change')

#     choices = [('weekly', 'Weekly'), ('monthly', 'Monthly'), ('never', 'Never')]
#     fr.add_select_field('update_freq', choices, default='daily')

#     fr.add_section(
#         'Price Alert',
#         'Get notified when a coin crosses above or below a price target.',
#         [
#             (FormBuilder.TEXT, 'Above'),
#             (FormBuilder.CONTROL, 'above_value'),
#             (FormBuilder.TEXT, 'Below'),
#             (FormBuilder.CONTROL, 'below_value')
#         ]
#     )
#     fr.add_section(
#         'Percentage Price Alert',
#         'Get notified when a coin changes in value by a specific percent.',
#         [
#             (FormBuilder.TEXT, 'Changes'),
#             (FormBuilder.CONTROL, 'pct_change'),
#             (FormBuilder.TEXT, '%')
#         ]
#     )
#     fr.add_section(
#         'Periodic Update',
#         'Get notified of the price of an asset at regular intervals. Does not affect alert frequency. Alerts happen daily regardless of this setting.',
#         [
#             (FormBuilder.TEXT, 'Send status updates'),
#             (FormBuilder.CONTROL, 'update_freq')
#         ]
#     )

#     if request.method == 'POST':
#         (valid, error_msg) = fr.form_data_valid()
#         if not valid:
#             fr.add_section(
#                 None, None,
#                 [
#                     (FormBuilder.WARNING, "ERROR: Fix values marked in RED")
#                 ]
#             )

#     post_url = url_for("uilib_tests.test_form_builder")
#     body2 = fr.render(post_url)

#     body = body1 + "<br><br>" + body2

#     return rh.render_tmpl(
#         templates_dir,
#         default_page_tmpl,
#         get_page_attrs(body, footer_scripts="")
#     )


# @uilib_tests_blp.route("/test-form_submit-page", methods=['POST'])
# def test_form_submit_page():

#     if request.method == 'POST':
#         print(request.form)



# @uilib_tests_blp.route("/test-form-page", methods=['GET', 'POST'])
# def test_form_page():

#     if request.method == 'POST':
#         #print(request.form)
#         redirect_url = request.form.get('_redirect_url', None)
#         if redirect_url is not None:
#             print("Redirecting to ", redirect_url)
#             return redirect(redirect_url, code=302)
    
#     pb = PageBuilder()

#     css_id = 'basic_form2'
#     post_url = url_for("uilib_tests.test_form_page")
#     cancel_url = None
#     redirect_url = url_for("uilib_tests.tests_home_page")
#     form = FormComponent(css_id, redirect_url=redirect_url, post_url=post_url, cancel_url=cancel_url)

#     field = FormTextField(
#         name='name', 
#         label='Name', 
#         help='The persons names.', 
#         required=True)
#     form.add_field(field)

#     field = FormNumberField(
#         name='age', 
#         label='Age', 
#         help='The persons age.', 
#         required=True, min=1, max=100)
#     form.add_field(field)

#     pb.add(form)
    
#     return pb.render()

@uilib_tests_blp.route("/test-htmx-api", methods=['GET'])
def test_htmx_api_page():
    i = random.randint(1, 1000)
    #time.sleep(1)
    html = '''
        <p>API Response %d</p>
    ''' % i
    return html

def get_form():
    html4 = '''
        <form id="example-form" hx-post="%s">
            <input type="text" id="value1" name="value1" placeholder="type w">
            <input type="text" id="value2" name="value2" placeholder="type w">
            <button type="submit">Click Me!</button><br><br>
        </form>
    ''' % url_for("uilib_tests.test_htmx_add_object_component")
    return html4

@uilib_tests_blp.route("/test-htmx-add_object-component", methods=['GET', 'POST'])
def test_htmx_add_object_component():
    i = random.randint(1, 1000)
    #time.sleep(1)
    if request.method == 'POST':
        print("POST:", request.form)
        #redirect_url = request.form.get('_redirect_url', None)
        # redirect_url = url_for("uilib_tests.test_htmx_page")
        # if redirect_url is not None:
        #     print("Redirecting to ", redirect_url)
        #     return redirect(redirect_url, code=302)

    html = get_form()
    return html

# @uilib_tests_blp.route("/test-carousel", methods=['GET'])
# def test_carousel_page():
#     html = """
#    <div id="carouselExampleIndicators" class="carousel slide" data-bs-ride="carousel">
#       <div class="carousel-indicators">
#         <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
#         <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
#         <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
#       </div>
#       <div class="carousel-inner">
#         <div class="carousel-item active">
#           <img src="https://via.placeholder.com/800x400.png?text=Slide+1" class="d-block w-100" alt="Slide 1">
#         </div>
#         <div class="carousel-item">
#           <img src="https://via.placeholder.com/800x400.png?text=Slide+2" class="d-block w-100" alt="Slide 2">
#         </div>
#         <div class="carousel-item">
#           <img src="https://via.placeholder.com/800x400.png?text=Slide+3" class="d-block w-100" alt="Slide 3">
#         </div>
#       </div>
#       <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
#         <span class="carousel-control-prev-icon" aria-hidden="true"></span>
#         <span class="visually-hidden">Previous</span>
#       </button>
#       <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
#         <span class="carousel-control-next-icon" aria-hidden="true"></span>
#         <span class="visually-hidden">Next</span>
#       </button>
#     </div>
#     """
#     js = '''
#     <script>
#         $(document).ready(function() {
#             $('#carouselExampleIndicators').carousel();
#         });
#     </script>
#     '''
#     return html + js

@uilib_tests_blp.route("/test-htmx-slideshow-api", methods=['GET'])
def test_htmx_slideshow_api_page():
    slide_index = int(request.args.get('index', 0))
    slides = [
        {"title": "Slide 1", "content": "Content for slide 1"},
        {"title": "Slide 2", "content": "Content for slide 2"},
        {"title": "Slide 3", "content": "Content for slide 3"}
    ]
    
    if slide_index < len(slides):
        slide = slides[slide_index]
        next_index = slide_index + 1
        api_url = url_for("uilib_tests.test_htmx_slideshow_api_page")
        
        html = f'''
            <h2>{slide['title']}</h2>
            <p>{slide['content']}</p>
            <p>Slide {slide_index + 1} of {len(slides)}</p>
        '''
        
        if next_index < len(slides):
            html += f'''
                <button id="next-slide"
                    hx-get="{api_url}?index={next_index}"
                    hx-trigger="click"
                    hx-target="#slide-content"
                    hx-swap="innerHTML">
                    Next Slide
                </button>
            '''
    else:
        html = '<p>Slideshow finished!</p>'
    
    time.sleep(1)
    return html

@uilib_tests_blp.route("/test-htmx-slideshow", methods=['GET'])
def test_htmx_slideshow_page():
    api_url = url_for("uilib_tests.test_htmx_slideshow_api_page")
    html = f'''
        <div id="slideshow">
            <div id="slide-content"
                 hx-get="{api_url}" 
                 hx-trigger="load"
                 hx-swap="innerHTML"
                 hx-indicator="#spinner">
            </div>
            <br><br>
            <div id="spinner" class="htmx-indicator">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>

        </div>
    '''
    
    pb = PageBuilder()
    c = HTMLComponent(html)
    pb.add(c)

    return pb.render()

@uilib_tests_blp.route("/test-htmx-page", methods=['GET'])
def test_htmx_page():
    api_url = url_for("uilib_tests.test_htmx_api_page")
    i = random.randint(1, 1000)
    html = '''
        <div id="parent-div">
            <p>Test: hx-swap = afterend</p>
        </div>
        <button hx-get="%s"
            hx-trigger="click"
            hx-target="#parent-div"
            hx-swap="afterend">
            Click Me! %d
        </button><br><br>
    ''' % (api_url, i)

    html2 = '''
        <div id="parent-div-2">
            <p>Test: hx-swap = innerHTML</p>
        </div>
        <button hx-get="%s"
            hx-trigger="click"
            hx-target="#parent-div-2"
            hx-swap="innerHTML"
            hx-indicator="#indicator"
        >
            Click Me!
        </button><br><br>
    ''' % api_url

    html3 = '''
        <button class="btn btn-primary" type="button" disabled>
            <div>
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span class="sr-only">Loading...</span>
            </div>
        </button>

    '''

    html4 = test_htmx_add_object_component()

    # '''
    # hx-post="%s"
    #         hx-trigger="click"
    #         hx-target="#parent-div-2"
    #         hx-swap="innerHTML"
    #         hx-indicator="#indicator"
    # '''
    pb = PageBuilder()

    c = HTMLComponent(html)
    pb.add(c)


    c = HTMLComponent(html2)
    pb.add(c)

    spinner = '''
        <div id="indicator" class="spinner-border htmx-indicator" role="status">
            <span class="sr-only"></span>
        </div><br><br>
    '''
    #c = HTMLComponent(spinner)
    #pb.add(c)

#    c = HTMLComponent(html3)
#    pb.add(c)

    c = HTMLComponent(html4)
    pb.add(c)

    return pb.render()


# @uilib_tests_blp.route("/test-alert_page", methods=['GET', 'POST'])
# def test_alert_page():

#     #--------------------------

#     fb = FormBuilder(request)
#     #fb.add_text_field('search')

#     c = Container(cols=1)
#     c.add_element(TextHeading('Search'))
#     c.add_element(ParagraphText('Enter one or more asset names or symbols separated by commas.'))
#     c.add_element(TextField(id='search'))
#     c.add_element(LineBreak())
#     c.add_element(ParagraphText('Popular Search Terms:'))
#     c.add_element(Badges(['Bitcoin (BTC)', 'Bitcoin (BTC)', 'Bitcoin (BTC)', 'Bitcoin (BTC)', 'Bitcoin (BTC)', 'Bitcoin (BTC)', 'Bitcoin (BTC)']))
#     body = c.render()

#     #--------------------------

#     # fr = FormBuilder(request)
#     # fr.add_decimal_field('above_value')
#     # fr.add_decimal_field('below_value')
#     # fr.add_decimal_field('pct_change')
#     #
#     # choices = [('weekly', 'Weekly'), ('monthly', 'Monthly'), ('never', 'Never')]
#     # fr.add_select_field('update_freq', choices, default='daily')
#     #
#     # fr.add_section(
#     #     'Price Alert',
#     #     'Get notified when a coin crosses above or below a price target.',
#     #     [
#     #         (FormBuilder.TEXT, 'Above'),
#     #         (FormBuilder.CONTROL, 'above_value'),
#     #         (FormBuilder.TEXT, 'Below'),
#     #         (FormBuilder.CONTROL, 'below_value')
#     #     ]
#     # )
#     # fr.add_section(
#     #     'Percentage Price Alert',
#     #     'Get notified when a coin changes in value by a specific percent.',
#     #     [
#     #         (FormBuilder.TEXT, 'Changes'),
#     #         (FormBuilder.CONTROL, 'pct_change'),
#     #         (FormBuilder.TEXT, '%')
#     #     ]
#     # )
#     # fr.add_section(
#     #     'Periodic Update',
#     #     'Get notified of the price of an asset at regular intervals. Does not affect alert frequency. Alerts happen daily regardless of this setting.',
#     #     [
#     #         (FormBuilder.TEXT, 'Send status updates'),
#     #         (FormBuilder.CONTROL, 'update_freq')
#     #     ]
#     # )
#     #
#     # if request.method == 'POST':
#     #     (valid, error_msg) = fr.form_data_valid()
#     #     if not valid:
#     #         fr.add_section(
#     #             None, None,
#     #             [
#     #                 (FormBuilder.WARNING, "ERROR: Fix values marked in RED")
#     #             ]
#     #         )
#     #
#     # post_url = url_for("uilib_tests.test_form_builder")
#     # body2 = fr.render(post_url)

#     post_url = url_for("uilib_tests.test_form_builder")
#     #body = fb.render(post_url)

#     return rh.render_tmpl(
#         templates_dir,
#         default_page_tmpl,
#         get_page_attrs(body, footer_scripts="")
#     )

# @uilib_tests_blp.route('/submit', methods=['GET', 'POST'])
# def submit():
#     form = MyForm()
#     if form.validate_on_submit():
#         return redirect('/success')
#     return render_template('submit.html', form=form)


# # Show an example graph from the dygraph library
# @uilib_tests_blp.route("/test-search-data-api")
# def test_search_data_api():
#     search = request.args.get('search', None)
#     corpus = {
#         'BTC': "Bitcoin (BTC)",
#         'ETH': "Ethereum (ETH)",
#         'USDT': "Tether (USDT)",
#         'XRP': "XRP (XRP)",
#         'BNB': "Binance Coin (BNB)",
#         'LCT': "Litecoin (LTC)",
#         'DOGE': "Dogecoin (DOGE)",

#     }
#     dct = []
#     search = search.lower()
#     for key, label in corpus.items():
#         if search in label.lower():
#             dct.append({'label': label})

#     j = json.dumps(dct, indent=4)
#     response = Response(j, status=200, mimetype="application/json")
#     return response

# @uilib_tests_blp.route("/test-autocomplete-basic")
# def test_autocomplete_basic_page():

#     html = "<h2>Autocomplete Basic Test</h2>"

#     data_url = url_for("uilib_tests.test_search_data_api")
#     a = ac.Autocomplete()
#     (ac_html, ac_js) = a.render_basic(data_url)
#     head_scripts = a.get_head_scripts()
#     css_links = a.get_css_links()

#     html = html + ac_html
#     return rh.render_tmpl(
#         templates_dir,
#         default_page_tmpl,
#         get_page_attrs(html, head_scripts=head_scripts, footer_scripts=ac_js, css_links=css_links),
#     )

# @uilib_tests_blp.route("/test-autocomplete")
# def test_autocomplete_page():

#     title = "Test Page"
#     html = "<h2>Autocomplete Test</h2>"
#     # html += "<p>Fetches data from the Breaking Bad api site</p>"
#     #
#     # head_scripts_url = url_for("statics_page.static_file", file='autocomplete.min.js')
#     # head_scripts = "<script src='%s'></script>" % head_scripts_url
#     #
#     # css_url = url_for("statics_page.static_file", file='autocomplete.min.css')
#     # css_links = "<link rel='stylesheet' href='%s'>" % css_url
#     #
#     # html += '''
#     # <div class="auto-search-wrapper">
#     #     <input type="text" id="basic" placeholder="type w">
#     # </div>
#     # '''
#     # js = '''
#     # <script type="text/javascript">
#     #     new Autocomplete("basic", {
#     #       onSearch: ({ currentValue }) => {
#     #         const api = `https://breakingbadapi.com/api/characters?name=${encodeURI(
#     #           currentValue
#     #         )}`;
#     #         return new Promise((resolve) => {
#     #           fetch(api)
#     #             .then((response) => response.json())
#     #             .then((data) => {
#     #               resolve(data);
#     #             })
#     #             .catch((error) => {
#     #               console.error(error);
#     #             });
#     #         });
#     #       },
#     #
#     #       onResults: ({ matches }) =>
#     #         matches.map((el) => `<li>${el.name}</li>`).join(""),
#     #     });
#     # </script>
#     # '''

#     data_url = url_for("uilib_tests.test_search_data_api")

#     a = ac.Autocomplete()
#     (ac_html, ac_js) = a.render(data_url)
#     head_scripts = a.get_head_scripts()
#     css_links = a.get_css_links()

#     html = html + ac_html
#     js = ac_js
#     return rh.render_tmpl(
#         templates_dir,
#         default_page_tmpl,
#         get_page_attrs(html, head_scripts=head_scripts, footer_scripts=js, css_links=css_links),
#     )
