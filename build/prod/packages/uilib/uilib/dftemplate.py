import pandas as pd
import numpy as np
from uilib.renderresponse import RenderResponse
import datetime

class DFTemplate:
    def __init__(self,
        submit_url='_self', 
        submit_get_param='ids',
        add_checkboxes=False):

        self.css_classes_df = pd.DataFrame()
        self.submit_url = "%s?%s=" % (submit_url, submit_get_param)
        self.add_checkboxes=add_checkboxes
        self.button_label='Submit'

    def build_tmpl(self, css_id, header, body, striped=True):
        if striped:
            striped_str = "table-striped"
        else:
            striped_str = ""
        tbl = (
            "<table id='%s' class='table %s table-bordered table-hover' cellspacing='0' width='100%s'>"
            % (css_id, striped_str, "%")
        )
        if len(header) > 0:
            tbl += "<thead>%s</thead>" % header

        tbl += "<tbody>%s</tbody>" % body
        tbl += "</table>"
        return tbl

    def get_header(self, show_columns, show_idx=True, column_headers_replace_underscores=True):
        header = ["<tr>"]
        if self.add_checkboxes:
            header.append("<th scope='col'>&nbsp;</th>")
        if show_idx:
            header.append("<th scope='col'>index</th>")
        for col, label in show_columns:
            if column_headers_replace_underscores:
                label = label.replace("_", " ")
            header.append("<th scope='col'>%s</th>" % label)
        return "".join(header)


    def format_datetime(self, value):
        #print("format_datetime: '%s', '%s'" % (value, type(value)))
        if value is None or pd.isna(value):
            return ""
        
        if type(value) == float:
            try:
                value = int(value)
            except:
                return ""
            
        if type(value) == int:
            if value < 1000:
                return ""
            value = datetime.datetime.fromtimestamp(value)
            s = value.strftime("%Y-%m-%d %I:%M %p")
            return s        
        try:
            return value.strftime("%Y-%m-%d %I:%M %p")
        except:
            pass
        
        return value

    # {
    #         "added ts": {
    #             "fmt": "datetime",
    #             "wrap": False,
    #         },
    # },
    def _format_cell(self, col_key, cell_value, cell_formats):
        cell_format = cell_formats.get(col_key, None)
        if cell_format is None:
            return cell_value
        
        cell_fmt = cell_format.get("fmt", None)
        if cell_fmt == "datetime":
            cell_value = self.format_datetime(cell_value)
        if cell_fmt == "int":
            try:
                cell_value = int(cell_value)
            except:
                cell_value = ""

        cell_wrap = cell_format.get("wrap", True)
        if not cell_wrap:
            cell_value = "<span style='white-space: nowrap;'>%s</span>" % cell_value
            
        return cell_value

    def get_body(
        self,
        df,
        show_index=True,
        cell_styler=None,
        cell_value_formatter=None,
        cell_formats=None,
        show_columns=None
    ):
        
        rows = []
        if df is None:
            return "<tr></tr>"
        for ridx, row in df.iterrows():
            r = ["<tr>"]
            if self.add_checkboxes:
                r.append("<td><input type='checkbox' name='select'  id='1' value='%s'></td>" % ridx)
            if show_index:
                r.append("<td>%s</td>" % ridx)
                    
            for col_key, label in show_columns:
                cell_value = row.get(col_key, '')
                cell_value_formatted = cell_value
                #print("Col Key %s, Label %s, Value %s" % (col_key, label, cell_value))

                if cell_formats is not None:
                    print("Cell Formats not None")
                    cell_html = self._format_cell(col_key, cell_value, cell_formats)
                    cell = "<td>%s</td>" % cell_html
                else:
                    if cell_value_formatter is not None:
                        #print("Cell Value Formatter not None")
                        cell_value_formatted = cell_value_formatter.format(col_key, cell_value)
                    if cell_styler is not None:
                        #print("Cell Styler not None")
                        cell_styles = cell_styler.get_style(ridx, col_key, cell_value)
                        #print("Cell value formatted %s" % cell_value_formatted)
                        cell = "<td %s>%s</td>" % (cell_styles, cell_value_formatted)
                    else:
                        #print("Cell Styler None")
                        cell = "<td>%s</td>" % cell_value_formatted

                r.append(cell)
            r.append("</tr>")
            rows.append("".join(r))
        return "".join(rows)

    def get_ready_js(self, css_id, show_search):
        js = ["<script>"]
        js.append("$(document).ready(function() {")
        js.append("$('#%s').DataTable( {" % css_id)
        js.append('"aaSorting": [],')
        if show_search:
            search_str = "true"
        else:
            search_str = "false"

        if self.add_checkboxes:
            # disable sorting on the checkbox column
            js.append('"columnDefs": [{ "orderable": false, "targets": 0 }],')

        js.append('"searching": %s,' % search_str)
        js.append('"paging": false,')
        js.append('"info": false')
        js.append("});")
        js.append("});")
        js.append("</script>")
        return "".join(js)

    def get_submit_form_js(self):
        js = '''
            <script>
                function submitForm() {
                    console.log('Form Submitted');
                    // Get all checkboxes in the form
                    const table = document.querySelector('#%s');
                    var checkboxes = table.querySelectorAll('input[type="checkbox"]');
                    
                    // Get the values of the checked checkboxes
                    var values = [];
                    for (var i = 0; i < checkboxes.length; i++) {
                        if (checkboxes[i].checked) {
                        values.push(checkboxes[i].value);
                        }
                    }
                    
                    // Construct the new URL with the values as query parameters
                    // var url = 'new_page.html?' + encodeURIComponent(values.join(','));
                    var url = '%s' + values.join(',');

                    // Redirect the user to the new page
                    //window.location.href = url;
                    console.log(values);
                    console.log(url);
                }
            <script>
        ''' 
        #% (css_id, self.submit_url)
        return js

    def get_check_all_checkboxes_js(self):
        js = '''
            <script>
                function selectAllCheckboxes(selectAllCheckbox) {
                const table = document.getElementById('%s');
                const checkboxes = table.querySelectorAll('input[type="checkbox"]');
                for (let checkbox of checkboxes) {
                    if (checkbox !== selectAllCheckbox) { // Skip the master checkbox itself
                        checkbox.checked = selectAllCheckbox.checked;
                    }
                }
            }
            </script>
        ''' 
        #% (css_id)
        return js

    def render(
        self,
        df,
        css_id,
        title=None,
        sub_title=None,
        show_search=True,
        show_index=True,
        striped=True,
        cell_styler=None,
        cell_value_formatter=None,
        cell_formats=None,
        show_columns=True,
        view_all_button_label = "View All",
        view_all_button_url = None,
        column_headers_replace_underscores=True,
        selector_buttons=None,
        show_header=True,
    ):
        
        response = RenderResponse()

        #html_elements = []
        if title is not None:
            response.add_html("<h2>%s</h2>" % title)


        #if sub_title is not None:
        #    response.add_html("%s" % sub_title)

        if selector_buttons is not None:
            buttons_html = []
            for (url, label) in selector_buttons:
                button_html = f"""
                <a class="btn btn-outline-dark btn-sm" href='{url}' style='text-decoration: none;'>{label}</a>
                """
                buttons_html.append(button_html)
            buttons_html = "&nbsp;".join(buttons_html)
        else:
            buttons_html = ""

        sub_title_tmpl = f"""
            <div class='mb-2' style="display: flex; justify-content: space-between; align-items: center;">
                <div>{sub_title if sub_title else ''}</div>
                <div class="text-end">{buttons_html}</div>
            </div>
        """

        response.add_html(sub_title_tmpl)

        if title is None:
            title = ""
        if df is None or len(df.index) == 0:
            html = title + "<br>" + "Empty"
            response.add_html(html)

        if show_columns is None:
            show_columns = []
            for col in df.columns:
                show_columns.append((col,col))

        if show_header:
            header = self.get_header(show_columns, show_index, column_headers_replace_underscores)
        else:
            header = ""

        body = self.get_body(
            df,
            show_index=show_index,
            cell_styler=cell_styler,
            cell_value_formatter = cell_value_formatter,
            cell_formats=cell_formats,
            show_columns = show_columns,
        )
        js = self.get_ready_js(css_id, show_search)
        response.add_footer_js(js)

        table_html = self.build_tmpl(css_id, header, body, striped)

        if self.add_checkboxes:  
            table_html = '''
                <form method='get' target='%s'>
                    %s
                    <button class='btn btn-secondary btn-sm' onclick='submitForm("%s")'>%s</button>
                </form>
            ''' % (self.submit_url, table_html, self.button_label, css_id)

            response.add_footer_js(self.get_submit_form_js())
            response.add_footer_js(self.get_check_all_checkboxes_js())

            # const selectedCheckboxes = Array.from(checkboxes).filter(cb => cb.checked).map(cb => cb.value);
            # const urlParams = new URLSearchParams(selectedCheckboxes);
            # window.location.href = `/new-page?${urlParams}`;
            #html_elements.append(table_html)

        response.add_html(table_html)

        if view_all_button_url is not None:
            view_all_button_html = '''
                <div style='margin-top: 20px; text-align: right;'>
                    <a class = "btn btn-outline-dark btn-sm" href='%s'>%s</a>
                </div>
            ''' % (view_all_button_url, view_all_button_label)
            response.add_html(view_all_button_html)


        #return ("\n".join(html_elements), js)
        return response
    
    # This is the Javascript that should only be included once in the page
    def get_global_js():
        return ''