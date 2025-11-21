from uilib.dataframeformatter import DataFrameFormatter
from uilib.dftemplate import DFTemplate
from uilib.formathelpers import *
from uilib.renderresponse import RenderResponse


class Component:
    def __init__(self):
        pass

    def render(self):
        return RenderResponse()






















#    html = "<br><p class='page_cat'>%s</p>" % page_type
#     for k, v in headings.items():
#         html += "<p class='page_item'>%s: %s</p>" % (k, v)
#     html += "<br>"
#     for k, v in attrs.items():
#         html += "%s: %s<br>" % (k, v)
#     html += "<br>"
#     return html








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


class TabsComponent(Component):
    def __init__(self, tabs, selected_id, view='tabs', aligned_right=True):
        self.tabs = tabs
        self.selected_id = selected_id
        self.view = view
        self.aligned_right = aligned_right

    def render(self):
        # Add custom CSS for darker borders
        css = """
            <style>
                .nav-tabs {
                    border-bottom: 1px solid #dee2e6;
                }
                .nav-tabs .nav-link {
                    border-color: #f8f9fa #f8f9fa #dee2e6;
                    color: #6c757d;
                    border: 1px solid transparent;
                    margin-bottom: -1px;
                }
                .nav-tabs .nav-link.active {
                    border-color: #AAAAAA;
                    border-bottom: 0px;
                    color: #495057;
                    font-weight: 500;
                    background-color: #f8f9fa;
                }
                .nav-tabs .nav-link:hover:not(.active) {
                    border-color: border-color: #AAAAAA;
                    isolation: isolate;
                }
            </style>
        """

        # Add justify-content-end class if aligned_right is True
        alignment_class = " justify-content-end" if self.aligned_right else ""

        if self.view == 'pills':
            html = f"<ul class='nav nav-pills{alignment_class}'>"
        else:
            html = css + f"<ul class='nav nav-tabs{alignment_class}'>"

        for id, label, link in self.tabs:
            html += "<li class='nav-item'>"
            if id == self.selected_id:
                html += (
                    "<a class='nav-link active' aria-current='page' href='%s'>%s</a>"
                    % (link, label)
                )
            else:
                html += "<a class='nav-link' href='%s'>%s</a>" % (link, label)
            html += "</li>"
        html += "</ul>"
        return RenderResponse(html=html)

    # def render(self):
    #     tabs = []
    #     #view_info = []
    #     #for view in views:
    #     #    view_info.append((view, view))
    #     #for view in view_info:
    #     #    selected = view[1] == selected_view
    #     #    url = url_for("dataset_page", dataset_id=dataset_id, view=view[1])
    #     #    tabs.append({"label": view[0], "link": url, "selected": selected})
    #     tabs_html = render_tabs(tabs)
    #     return tabs_html


class TimeseriesChart:
    def __init__(
        self,
        df,
        chart_num,
        y_columns,
        y_axis_label,
        x_column=None,
        height="600px",
        show_legend=True,
        title=None,
        sub_title="Yadda Yadda",
    ):
        self.df = df.copy()
        self.chart_num = chart_num
        self.x_column = x_column
        self.y_columns = y_columns
        self.title = title
        self.sub_title = sub_title
        self.y_axis_label = y_axis_label
        self.height = height
        self.show_legend = show_legend

    def render(self):

        graph = BillboardChart(
            chart_num=self.chart_num,
            y_axis_label=self.y_axis_label,
            height=self.height,
            show_legend=self.show_legend,
        )

        graph.add_data_df(self.df, self.x_column, self.y_columns)

        css_links = BillboardChart.get_css_links()
        head_scripts = BillboardChart.get_head_scripts()

        html = f"<h2>{self.title}</h2>" if self.title is not None else "<br><br>"
        html += f"<small>{self.sub_title}</small>" if self.sub_title is not None else ""

        (chart_html, footer_scripts) = graph.render()
        html += chart_html

        return RenderResponse(
            html=html,
            header_js=head_scripts,
            footer_js=footer_scripts,
            css_links=css_links,
        )


class MultiPanelTimeseriesChart:
    def __init__(
        self,
        chart_num,
        panel_choices,
        initial_panel,
        title="Graph Title",
        sub_title="Graph SubTitle",
        y_axis_label="Y Axis",
        height="600px",
        show_legend=True,
    ):
        self.chart_num = chart_num
        self.title = title
        self.sub_title = sub_title
        self.y_axis_label = y_axis_label
        self.height = height
        self.show_legend = show_legend
        self.panel_choices = panel_choices
        self.initial_panel = initial_panel

    def _generate_radio_buttons(self, chart_num, update_func_name, buttons, selected):
        html = (
            '<div class="btn-group btn-group-sm" role="group" aria-label="Buttons for Chart %d">\n'
            % chart_num
        )
        for i, (label, url) in enumerate(buttons, start=1):
            checked = " checked" if label == selected else ""
            # name = 'chart_%d_btn_%s' % (chart_num, label.lower().replace(' ', '_'))
            name = "chart_%d_btn" % (chart_num)
            id = "%s_%d" % (name, i)
            html += f'  <input type="radio" class="btn-check" name="{name}" id="{id}" autocomplete="off"{checked}>\n'
            html += f'  <label class="btn btn-outline-primary" for="{id}" onclick="{update_func_name}(\'{url}\')">{label}</label>\n'
        html += "</div>"
        return html

    def render(self):
        from uilib.components.billboardchart import BillboardChart

        # search through panels to find the url that matches initial pannel
        initial_data_url = next(
            (url for label, url in self.panel_choices if label == self.initial_panel),
            None,
        )

        graph = BillboardChart(
            chart_num=self.chart_num,
            y_axis_label=self.y_axis_label,
            height=self.height,
            show_legend=self.show_legend,
            data_url=initial_data_url,
        )

        css_links = BillboardChart.get_css_links()
        head_scripts = BillboardChart.get_head_scripts()

        title_html = f"<h2>{self.title}</h2>" if self.title else ""
        sub_title_html = f"<small>{self.sub_title}</small>" if self.sub_title else ""

        update_func_name = "updateChart%dData" % self.chart_num

        buttons_html = self._generate_radio_buttons(
            self.chart_num, update_func_name, self.panel_choices, self.initial_panel
        )

        chart_header_tmpl = f"""
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        {title_html}
                        <p class="text-muted">{sub_title_html}</p>
                    </div>
                    {buttons_html}
                </div>
        """


        update_data_func_js = """
            <script>
            function %s(url) {
                fetch(url)
                    .then(response => response.text())
                    .then(data => {
                        chart%d.load({
		                    url: url
	                });
                })
                .catch(error => console.error('Error fetching data:', error));
            }
            </script>
            """ % (
            update_func_name,
            self.chart_num,
        )

        graph_response = graph.render()
        chart_html = graph_response.get_html()
        graph_footer_js = graph_response.get_footer_js()
        footer_js = graph_footer_js + "\n" + update_data_func_js
        html = chart_header_tmpl + chart_html

        return RenderResponse(
            html=html,
            header_js=head_scripts,
            footer_js=footer_js,
            css_links=css_links,
        )


class UpdatingTextBox(Component):
    def __init__(self, css_id, url):
        self.url = url
        self.css_id = css_id

    def _get_js(self, url, element_id, refresh_interval_secs=2):
        js = """
            const textBox = document.getElementById(%s);
            function pollAPI() {
            fetch('%s')
                .then(response => response.json())
                .then(data => {
                textBox.value = data.result;
                setTimeout(pollAPI, %d); // call the function again after 2 seconds
                })
                .catch(error => console.error(error));
            }
            pollAPI(); // start polling the API
        """ % (
            element_id,
            url,
            refresh_interval_secs * 1000,
        )
        return js

    def render(self):
        html = "<div id='%s'></div>" % (self.css_id)
        js = self._get_js(self.url, element_id=self.css_id)
        return RenderResponse(html=html, footer_js=js)


class FileUploadComponent(Component):

    def __init__(self, upload_url):
        self.upload_url = upload_url

    def _get_js(self):
        js = (
            """
         <script>
function _(el) {
  return document.getElementById(el);
}

function uploadFile() {
  var file = _("file").files[0];
  // alert(file.name+" | "+file.size+" | "+file.type);
  var formdata = new FormData();
  formdata.append("file", file);
  var ajax = new XMLHttpRequest();
  ajax.upload.addEventListener("progress", progressHandler, false);
  ajax.addEventListener("load", completeHandler, false);
  ajax.addEventListener("error", errorHandler, false);
  ajax.addEventListener("abort", abortHandler, false);
  ajax.open("POST", "%s"); 
  //use file_upload_parser.php from above url
  ajax.send(formdata);
}

function progressHandler(event) {
  _("loaded_n_total").innerHTML = "Uploaded " + event.loaded + " bytes of " + event.total;
  var percent = (event.loaded / event.total) * 100;
  _("progressBar").value = Math.round(percent);
  _("status").innerHTML = Math.round(percent) + "pct uploaded... please wait";
}

function completeHandler(event) {
  _("status").innerHTML = event.target.responseText;
  _("progressBar").value = 0; //wil clear progress bar after successful upload
}

function errorHandler(event) {
  _("status").innerHTML = "Upload Failed";
}

function abortHandler(event) {
  _("status").innerHTML = "Upload Aborted";
}
</script>
        """
            % self.upload_url
        )
        return js

    def render(self):
        # html = "<div id='%s'></div>" % (self.css_id)

        html = """
<form id="upload_form" enctype="multipart/form-data" method="post">
  <input type="file" name="file" id="file" onchange="uploadFile()"><br>
  <progress id="progressBar" value="0" max="100" style="width:300px;"></progress>
  <h3 id="status"></h3>
  <p id="loaded_n_total"></p>
</form>
        """
        js = self._get_js()
        return RenderResponse(html=html, footer_js=js)




class FooterComponent:
    def __init__(self, logo_src, logo_alt, footer_text, section_labels, sections):
        """
        Initialize the FooterComponent with dynamic content for customization.

        :param logo_src: The source URL for the logo image.
        :param logo_alt: The alternative text for the logo image.
        :param copyright_text: Copyright text to be displayed.
        :param section_labels: A list of labels for each section.
        :param sections: A list of lists, where each list contains tuples of URL and link text for that section.
        """
        self.logo_src = logo_src
        self.logo_alt = logo_alt
        self.footer_text = footer_text
        self.section_labels = section_labels
        self.sections = sections

    def render(self):
        # Helper function to build link lists
        def build_link_list(links):
            return "".join(
                f'<li class="mb-1"><a class="text-decoration-none footer-link" href="{url}">{text}</a></li>'
                for url, text in links
            )

        # Generate the HTML content for the footer component
        # <footer class="pt-4 my-md-5 pt-md-5 border-top footer mt-5">
        html = f"""
        <br><br>
        <footer class="footer mt-5">
            <div class="row">

            <div class="col-12 col-md">
                <img class="mb-2" src="{self.logo_src}" alt="{self.logo_alt}" width="50">
            </div>"""

        for label, section in zip(self.section_labels, self.sections):
            html += f"""
                <div class="col-6 col-md">
                    <h5 class='footer-links-header'>{label}</h5>
                    <ul class="list-unstyled text-small">
                    {build_link_list(section)}
                    </ul>
                </div>"""

        html += """</div>"""
        html += """<div class="row pt-4" style="text-align: center;">"""
        html += f"""<small class="d-block mb-3 text-muted">{self.footer_text}</small>"""
        # html += f'''<small class="d-block mb-3 text-muted">© {self.copyright_text}</small>'''
        html += """</div>"""
        html += """</footer>"""

        return RenderResponse(html=html)

    @staticmethod
    def example():

        # Example to instantiate and render the FooterComponent with custom links
        footer_component = FooterComponent(
            logo_src="/docs/5.0/assets/brand/bootstrap-logo.svg",
            logo_alt="Bootstrap Logo",
            footer_text="2017–2021",
            section_labels=["Section 1", "Section 2", "Section 3"],
            sections=[
                [("#", "Cool stuff"), ("#", "Random feature")],
                [("#", "Resource"), ("#", "Resource name")],
                [("#", "Team"), ("#", "Locations"), ("#", "Privacy"), ("#", "Terms")],
            ],
        )
        return footer_component


class SimpleFooterComponent:

    def __init__(self, site_name, links):
        self.links = links
        self.site_name = site_name

    def render(self):

        if len(self.links) == 0:
            links_body = ""
        else:
            links_html = ""
            for link in self.links:
                links_html += f'<li class="nav-item" style="padding: 10px; "><a href="{link["url"]}" class="footer-link">{link["name"]}</a></li>'

            links_body = f"""
                <ul class="nav justify-content-center">
                    {links_html}                
                </ul>
            """
        # <li class="nav-item"><a href="#" class="nav-link px-2 text-body-secondary">Home</a></li>
        html = f"""
            <footer class="footer pt-3 pb-2 mb-0">
                {links_body}
                <p class="text-center">© 2025 {self.site_name}</p>
            </footer>
            """
        return RenderResponse(html=html)


class NewsletterSubscribeComponent:

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






class PrivacyPolicyComponent:
    def __init__(self, file_path, home_url, company_name, contact_url):
        # Store the path to the HTML file and the company name to insert.
        self.file_path = file_path
        self.home_url = home_url
        self.contact_url = contact_url
        self.company_name = company_name

    def render(self):
        # Read the HTML file content
        try:
            with open(self.file_path, "r") as file:
                html_content = file.read()
        except FileNotFoundError:
            return RenderResponse(html="Error: File not found.", footer_js="")

        # Replace placeholder with the actual company name
        html_content = html_content.replace("{home_url}", self.home_url)
        html_content = html_content.replace("{company_name}", self.company_name)
        html_content = html_content.replace("{contact_url}", self.contact_url)

        # Since this component might not use JavaScript, we set it as an empty string
        javascript = ""

        return RenderResponse(html=html_content, footer_js=javascript)

    @staticmethod
    def example():
        # Provide an example usage of the PrivacyPolicyComponent.
        file_path = "/packages/uilib/uilib/statics/templates/privacy_policy.html"
        company_name = "Example Company"
        component = PrivacyPolicyComponent(file_path, company_name)
        return component


class AccordionComponent:
    def __init__(self, header, accordion_id, sections):
        """
        Initialize the AccordionComponent with dynamic sections for customization.

        :param accordion_id: The ID for the entire accordion component to ensure uniqueness in the DOM.
        :param sections: A list of dictionaries, each containing a 'title' and 'content' for each accordion item.
        """
        self.accordion_id = accordion_id
        self.sections = sections
        self.header = header

    def render(self):
        # Generate the HTML content for the accordion component
        html = f'<div class="accordion" id="{self.accordion_id}">'
        for index, section in enumerate(self.sections, start=1):
            is_expanded = "true" if index == 1 else "false"
            show_class = "show" if index == 1 else ""
            panel_id = f"{self.accordion_id}-collapse{index}"
            header_id = f"{self.accordion_id}-heading{index}"

            html += f"""
  <div class="accordion-item">
    <h2 class="accordion-header" id="{header_id}">
      <button class="accordion-button {'collapsed' if index != 1 else ''}" type="button" data-bs-toggle="collapse" data-bs-target="#{panel_id}" aria-expanded="{is_expanded}" aria-controls="{panel_id}">
        {section['title']}
      </button>
    </h2>
    <div id="{panel_id}" class="accordion-collapse collapse {show_class}" aria-labelledby="{header_id}">
      <div class="accordion-body">
        {section['content']}
      </div>
    </div>
  </div>"""
        html += "</div>"

        html = f"""
            <h1>{self.header}</h1>
            <br>
            {html}
        """
        return RenderResponse(html=html)

    @staticmethod
    def example():
        # Example usage of the AccordionComponent
        accordion_component = AccordionComponent(
            header="Example Accordion",
            accordion_id="accordionPanelsStayOpenExample",
            sections=[
                {
                    "title": "Accordion Item #1",
                    "content": "This is the first item's accordion body.",
                },
                {
                    "title": "Accordion Item #2",
                    "content": "This is the second item's accordion body.",
                },
                {
                    "title": "Accordion Item #3",
                    "content": "This is the third item's accordion body.",
                },
            ],
        )

        return accordion_component





class NewsletterSignupComponent:

    PITCH_TEXT = """Get information on new features, updates, and more. We respect your privacy. And we will never spam you. Unsubscribe at any time."""

    def __init__(self, post_url):
        # self.logo_src = logo_src
        # self.form_attrs = form_attrs
        # self.error_message = error_message
        # self.captcha_image_src = captcha_image_src
        self.post_url = post_url

    def get_input_group_html(post_url, error_msg=None):

        hx_target = "newsletter-email-div"

        htmx = f"""
            hx-post="{post_url}" hx-trigger="click" hx-target="#{hx_target}" hx-swap="outerHTML"
        """

        if error_msg is not None:
            error_html = f"""
                <p style='color: red;'>
                    {error_msg}
                </p>
            """
        else:
            error_html = ""

        html = f"""
            <div id="{hx_target}">
                <form method="post">
                    <div class="input-group">
                        <input id='email' name='email' type="email" class="form-control" placeholder="Enter your email" style='margin-right: 10px;'>
                        <span class="input-group-btn">
                            <button class="btn" {htmx} style='color: #fff; background: #243c4f;'>Subscribe Now</button>
                        </span>
                    </div>
                </form>
                {error_html}
            </div>
        """
        return html

    def render(self):

        input_group_html = NewsletterSignupComponent.get_input_group_html(
            self.post_url, None
        )

        html = f"""
        <section class="newsletter" style='padding: 80px 0; background: #d5e1df;'>
            <div class="container">
                <div class="row">
                    <div class="col-sm-12">
                        <div class="content">
                            <h2 style='color: dark-grey;'>Subscribe to our Newsletter</h2>
                            <p class="form-text">{NewsletterSignupComponent.PITCH_TEXT}</div>
                            
                                {input_group_html}
                            
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """
        return RenderResponse(html=html)

        header_text = "Newsletter Signup"
        button_text = "Signup"

        footer_lines = []
        controls = [
            {
                "id": "email",
                "label": "Email Address",
                "type": "email",
                "value": self.form_attrs.get("email", ""),
            }
        ]

        header_sub_text = "Subscribe to our newsletter. Get information on new features, updates, and more. We respect your privacy. And we will never spam you. Unsubscribe at any time."
        footer_text_lines = footer_lines

        logo_src = None
        logo_alt = None
        logo_height = None

        comp = VerticalFormComponent(
            logo_src,
            logo_alt,
            logo_height,
            header_text,
            header_sub_text,
            controls,
            button_text,
            footer_text_lines,
            add_captcha=False,
            error_msg=self.error_message,
            css_id="newsletter",
        )

        return comp.render()

    @staticmethod
    def example():
        pass


class NewsletterSignupVerticalFormComponent:

    def __init__(self, logo_src, form_attrs, error_message=None):
        self.logo_src = logo_src
        self.form_attrs = form_attrs
        self.error_message = error_message
        # self.captcha_image_src = captcha_image_src

    def render(self):

        header_text = "Newsletter Signup"
        header_sub_text = NewsletterSignupComponent.PITCH_TEXT
        button_text = "Subscribe Now"

        comp = VerticalFormComponent(
            logo_src=self.logo_src,
            header_text=header_text,
            header_sub_text=header_sub_text,
            button_text=button_text,
        )
        comp.add_email_field(id="email", label="Email Adress")
        return comp.render()

    @staticmethod
    def example():
        pass




class HeaderJsComponent:

    def __init__(self, header_js):
        self.header_js = header_js

    def render(self):
        return RenderResponse(header_js=self.header_js)


class ComboBoxComponent:

    def __init__(self, id, label, options, selected, post_url):
        self.id = id
        self.label = label
        self.options = options
        # self.value = value
        self.selected = selected
        self.post_url = post_url

    def render(self):

        # def generate_table_select_component(post_url, select_elements, selected_items):
        select_html = ""
        # for select_id, label_text, options in select_elements:

        select_html += f'<label for="{self.id}" class="me-2">{self.label}</label>'
        select_html += f'<select id="{self.id}" class="form-select me-4" name="{self.id}" hx-target="#rental-id" hx-indicator=".htmx-indicator" style="width: auto;">'
        for value, label in self.options:
            # selected_attr = ' selected' if self.id == selectedselected_items and selected_items[self.id] == value else ''
            selected_attr = ""
            select_html += f'<option value="{value}"{selected_attr}>{label}</option>'
        select_html += "</select>"

        html = f"""
            <div class="container mt-5">
                <div class="row">
                    <div class="col-12 d-flex justify-content-end">
                        <form class="d-flex align-items-center" action="{self.post_url}" method="POST">
                            {select_html}
                            <button type="submit" class="btn btn-primary">Submit</button>
                        </form>
                    </div>
                </div>
            </div>
        """
        return RenderResponse(html=html)

