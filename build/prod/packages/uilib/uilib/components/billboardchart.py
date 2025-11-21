

import json
import random

from flask import (
    url_for
)
from ..basecomponents import Component
from ..renderresponse import RenderResponse
# Example of setting series visibility
# https://dygraphs.com/tests/visibility.html

class BillboardChart(Component):

    def __init__(self, chart_num, y_axis_label, show_legend=True, height='600px', data_url=None):
        self.chart_num = chart_num
        self.y_axis_label = y_axis_label
        self.series = []
        self.height = height
        self.show_legend = show_legend
        self.data_url = data_url
        self.css_id = 'chart%d' % chart_num

        # self.fill = {
        #     "series": {
        #     }
        # }
        # self.options = {
        #     'legend': 'always',
        #     'labelsSeparateLines': False,
        #     'stepPlot': False,
        #     #'labelsDiv': 'labels3',
        #     #'legendFormatter': 'legendFormatter'
        #
        #     # 'highlightCircleSize': 2,
        #     # 'strokeWidth': 1,
        #     # 'highlightSeriesOpts': {
        #     #     'strokeWidth': 3,
        #     #     'strokeBorderWidth': 1,
        #     #     'highlightCircleSize': 5
        #     # }
        # }

    def add_data_df(self, df, x_column, y_columns):
        if x_column is None:
            data = list(df.index)
        else:
            data = list(df[x_column])
        #data_csv = ','.join(map(str, data))
        data_csv = ', '.join(['"%s"' % w for w in data])
        self.series.append("['%s', %s]" % ('x', data_csv))
        for col in y_columns:
            s = df[col].fillna(0)
            data = list(s)
            data_csv = ','.join(map(str, data))
            #data_csv = ', '.join(['"%s"' % w for w in data])
            self.series.append("['%s', %s]" % (col, data_csv))

    def get_data_block(self):
        return ",\n".join(self.series)

    # def _set_option(self, k, v):
    #     self.options[k] = v
    #
    # # def get_options_str(self):
    # #     # p = []
    # #     # for k,v in self.options.items():
    # #     #     if type(v) == str:
    # #     #         p.append("%s: '%s' " % (k,v))
    # #     #     else:
    # #     # return ",".join(p)
    # #     return json.dumps(self.options)
    #
    # def add_series_fill(self, series_name):
    #     self.fill['series'][series_name] = { 'fillGraph': True }

    def get_random_ts(length, width):
        d = []
        t = random.randint(25, 500)
        for i in range(0, length):
            d.append(str(t))
            t += random.randint(-width, +width)
        return ",".join(d)

    # def _render_chart(self):
    #     html = "<div id='%s' style='width: %s; height: %s; margin-right: 50px;'></div>" % (self.css_id, '98%', self.height)
        
    #     # Generate sample data for the chart
    #     data_section = '''
    #         data: {
    #             columns: [
    #                 ['data1', 30, 200, 100, 400, 150, 250],
    #                 ['data2', 130, 100, 140, 200, 150, 50]
    #             ],
    #             type: "line"
    #         },
    #     '''
        
    #     tick_format = "%Y-%m-%d"
    #     show_legend_str = 'true' if self.show_legend else 'false'
        
    #     footer_scripts = """
    #         <script type="text/javascript">
    #             var chart = bb.generate({
    #                 %s
    #                 grid: {
    #                     x: {
    #                         show: true
    #                     },
    #                     y: {
    #                         show: true
    #                     }
    #                 },
    #                 point: {
    #                     focus: {
    #                         only: true
    #                     }
    #                 },
    #                 axis: {
    #                     x: {
    #                         type: "timeseries",
    #                         tick: {
    #                             fit: false,
    #                             count: 10,
    #                             format: "%s"
    #                         }
    #                     },
    #                     "y": {
    #                         "label": {
    #                             "text": "%s",
    #                             "position": "outer-middle"
    #                         },
    #                     },
    #                 },
    #                 zoom: {
    #                     enabled: true,
    #                     type: "drag"
    #                 },
    #                 legend: {
    #                     show: %s
    #                 },
    #                 bindto: "#%s"
    #             });
    #         </script>
    #     """ % (data_section, tick_format, self.y_axis_label, show_legend_str, self.css_id)
        
    #     return (html, footer_scripts)
    
    # def render(self):
    #     # Convert the tuple return to RenderResponse
    #     html, footer_scripts = self._render_chart()
    #     from ..renderresponse import RenderResponse
        
    #     # Include Billboard.js CSS and JavaScript
    #     css_links = '<link rel="stylesheet" href="/statics/billboard.min.css">'
    #     header_js = '<script src="https://d3js.org/d3.v6.min.js"></script><script src="/statics/billboard.min.js"></script>'
        
    #     return RenderResponse(html=html, footer_js=footer_scripts, css_links=css_links, header_js=header_js)
    
    
    def render(self):

        html = "<div id='%s' style='width: %s; height: %s'; margin-right: 50px'></div>" % (self.css_id, '98%', self.height)

        data_block = self.get_data_block()


        tick_format = "%Y-%m-%d"

        if self.show_legend:
            show_legend_str = 'true'
        else:
            show_legend_str = 'false'

        if self.data_url is None:
            data_section = '''
                data: {
                    x: "x",
                    columns: [
                        %s
                    ],
                    type: "line"
                },
            ''' % data_block
        else:
            data_section = '''
                data: {
                    x: "x",
                    url: "%s",
                    type: "line"
                },''' % self.data_url

        footer_scripts = '''
            <script type="text/javascript">
                var chart%d = bb.generate({
                    %s
                    grid: {
                        x: {
                            show: true
                        },
                        y: {
                            show: true
                        }
                    },
                    point: {
                        focus: {
                            only: true
                        }
                    },
                    axis: {
                        x: {
                            type: "timeseries",
                            tick: {
                                fit: false,
                                count: 10,
                                format: "%s"
                            }
                        },
                        "y": {
                            "label": {
                                "text": "%s",
                                "position": "outer-middle"
                            },
                        },
                    },
                    zoom: {
                        enabled: false,
                        type: "drag"
                    },
                    legend: {
                        show: %s
                    },
                    bindto: "#%s"
                });
            </script>
        ''' % (self.chart_num, data_section, tick_format, self.y_axis_label, show_legend_str, self.css_id)

        css_links = BillboardChart.get_css_links()
        head_scripts = BillboardChart.get_head_scripts()

        response = RenderResponse(html=html, footer_js=footer_scripts, 
                                  css_links=css_links, header_js=head_scripts)
        return response



    @classmethod
    def example(cls):
        import random
        import pandas as pd
        import numpy as np
        
        #data_url = url_for("uilib_tests.random_chart_data_page")
        #data_url = data_url + "?num_lines=3"
        #print("Data URL: ", data_url)
        
        # Create sample data
        chart = cls(
            chart_num=random.randint(1000, 9999),
            y_axis_label="Sample Data",
            show_legend=True,
            height='400px',
            data_url=url_for("uilib_tests.random_chart_data_page")
        )
        
        
        return chart




    def get_css_links():
        css_url = url_for("statics_page.static_file", file='billboard.min.css')
        return "<link rel='stylesheet' href='%s'>" % css_url

    def get_head_scripts():
        s = []
        s.append("<script src='https://d3js.org/d3.v6.min.js'></script>")
        head_scripts_url = url_for("statics_page.static_file", file='billboard.min.js')
        s.append("<script src='%s'></script>" % head_scripts_url)
        return "\n".join(s)


