

import json
from ..basecomponents import Component

# Example of setting series visibility
# https://dygraphs.com/tests/visibility.html

class DyGraphChart(Component):
    def __init__(self):
        self.fill = {
            "series": {
            }
        }
        self.options = {
            'legend': 'always',
            'labelsSeparateLines': False,
            'stepPlot': False,
            #'labelsDiv': 'labels3',
            #'legendFormatter': 'legendFormatter'

            # 'highlightCircleSize': 2,
            # 'strokeWidth': 1,
            # 'highlightSeriesOpts': {
            #     'strokeWidth': 3,
            #     'strokeBorderWidth': 1,
            #     'highlightCircleSize': 5
            # }
        }

    def _set_option(self, k, v):
        self.options[k] = v

    # def get_options_str(self):
    #     # p = []
    #     # for k,v in self.options.items():
    #     #     if type(v) == str:
    #     #         p.append("%s: '%s' " % (k,v))
    #     #     else:
    #     # return ",".join(p)
    #     return json.dumps(self.options)

    def add_series_fill(self, series_name):
        self.fill['series'][series_name] = { 'fillGraph': True }

    def render(self, title, data_url, css_id, height_pixels=540, width="95%", checkboxes=None):
        h = []
        legend_id = "legend_%s" % css_id
        h.append("<div id='%s' style='height: 48px;'>Yadda</div>" % legend_id)
        h.append("<div id='%s' style='width: %s; height: %dpx'></div>" % (css_id, width, height_pixels))

        if checkboxes is not None:
            idx = 0
            for label in checkboxes:
                h.append("<input type='checkbox' id='%d' checked='' onclick='change(this)'>" % idx)
                h.append("<label for='%d'>%s</label>" % (idx, label))
                idx += 1

        #h.append("<input type='checkbox' id='%d' checked='' onclick='toggleall(this)'>" % idx)
        #h.append("<label for='%d'>%s</label>" % (idx, "toggle"))

        html = "\n".join(h)

        if title is None:
            title=''
        else:
            title = "title: '%s'," % title

        if len(self.fill['series'].keys()) > 0:
            fill_str = json.dumps(self.fill)
        else:
            fill_str = ''

        options = self.options
        options['labelsDiv'] = legend_id
        options_str = json.dumps(self.options)

        footer_scripts = '''
        <script type="text/javascript">
            g = new Dygraph(
                document.getElementById("%s"),
                "%s",
                 %s
            );
            function setStatus() {
                document.getElementById("visibility").innerHTML = g.visibility().toString();
            }
            function change(el) {
                g.setVisibility(parseInt(el.id), el.checked);
                setStatus();
            }  
            function toggleall(el) {

            }
            </script>
        ''' % (
            css_id,
            data_url,
            options_str
        )
        return (html, footer_scripts)

    # var
    # table = document.getElementById('%s');
    # var
    # checkboxes = table.querySelectorAll('input[type=checkbox]');
    # var
    # val = checkboxes[0].checked;
    # for (var i = 0; i < checkboxes.length; i++)  {
    #     console.log('Hey');
    # checkboxes[i].checked = var;

    def get_css_links():
        return "<link rel='stylesheet' src='/static/dygraph/dygraph.css' />"

    def get_head_scripts():
        return '<script type="text/javascript" src="/static/dygraph/dygraph.min.js"></script>'


      #
      # g = new Dygraph(
      #       document.getElementById("div_g"),
      #       NoisyDataABC, {
      #         rollPeriod: 7,
      #         errorBars: true,
      #         visibility: [false, true, true]
      #       }
      #     );
      # setStatus();

    def render(self):
        # Convert the tuple return to RenderResponse
        html, js = self._render_chart()
        from ..renderresponse import RenderResponse
        return RenderResponse(html=html, footer_js=js)
    
    def _render_chart(self):
        # Use default parameters for the example
        import random
        title = "Sample Chart"
        data_url = "/api/chart-data"
        css_id = f"chart{random.randint(1000, 9999)}"
        height_pixels = 400
        width = "95%"
        checkboxes = ["Series 1", "Series 2"]
        
        h = []
        legend_id = "legend_%s" % css_id
        h.append("<div id='%s' style='height: 48px;'>Chart Legend</div>" % legend_id)
        h.append("<div id='%s' style='width: %s; height: %dpx'></div>" % (css_id, width, height_pixels))

        if checkboxes is not None:
            idx = 0
            for label in checkboxes:
                h.append("<input type='checkbox' id='%d' checked='' onclick='change(this)'>" % idx)
                h.append("<label for='%d'>%s</label>" % (idx, label))
                idx += 1

        html = "\n".join(h)

        if title is None:
            title=''
        else:
            title = "title: '%s'," % title

        if len(self.fill['series'].keys()) > 0:
            fill_str = json.dumps(self.fill)
        else:
            fill_str = ''

        options = self.options
        options['labelsDiv'] = legend_id
        options_str = json.dumps(options)

        js = f"""
        <script type="text/javascript">
            var g = new Dygraph(
                document.getElementById("{css_id}"),
                "{data_url}", {{
                    {title}
                    {fill_str}
                    {options_str}
                }}
            );
        </script>
        """
        
        return (html, js)
    
    @classmethod
    def example(cls):
        return cls()

