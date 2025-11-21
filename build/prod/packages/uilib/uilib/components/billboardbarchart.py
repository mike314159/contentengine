

import json
import random
import pandas as pd
from uilib.renderresponse import RenderResponse
from ..basecomponents import Component

from flask import (
    url_for
)

# Example of setting series visibility
# https://dygraphs.com/tests/visibility.html

class BillboardBarChart(Component):

    def __init__(self, chart_num, y_axis_label, df, columns, title_html=None, subtitle_html=None, 
                 x_axis_label_column=None, show_legend=True, height='600px', data_url=None):
        self.chart_num = chart_num

        # If this is none, use dataframe index for x-axis labels
        self.x_axis_label_column = x_axis_label_column
        self.title_html = title_html
        self.subtitle_html = subtitle_html
        self.y_axis_label = y_axis_label
        self.series = []
        self.height = height
        self.show_legend = show_legend
        self.data_url = data_url
        self.css_id = 'chart%d' % chart_num
        self.df = df.copy()
        self.columns = columns
        self._add_data_df(self.df, self.columns)

        if self.x_axis_label_column is None:
            categories = ['"%s"' % w for w in df.index]
        else:
            categories = ['"%s"' % w for w in df[self.x_axis_label_column]]
        #print(categories)
        self.categories_csv = ",\n".join(categories)

    def _add_data_df(self, df, columns):
        # if x_column is None:
        #     data = list(df.index)
        # else:
        #     data = list(df[x_column])
        #data_csv = ','.join(map(str, data))
        #data_csv = ', '.join(['"%s"' % w for w in data])
        #self.series.append("['%s', %s]" % ('x', data_csv))
        for col in columns:
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

 
    def render(self):

        if self.title_html is not None:
            title_html = "%s" % self.title_html
        else:
            title_html = ""

        if self.subtitle_html is not None:
            subtitle_html = "%s" % self.subtitle_html
        else:
            subtitle_html = ""

        html = "%s%s<div id='%s' style='width: %s; height: %s'; margin-right: 50px;'>%s</div>" %  (title_html, subtitle_html, 
                                                                                                 self.css_id, '97%', self.height, title_html)

        data_block = self.get_data_block()

        tick_format = "%Y-%m-%d"

        if self.show_legend:
            show_legend_str = 'true'
        else:
            show_legend_str = 'false'

        # data_block = """
        #     ['data1', 30, 200, 100, 400, 150, 250],
        #     ['data2', 130, 100, 140, 200, 150, 50]
        # """
        # if self.data_url is None:
        #     data_section = '''
        #         data: {
        #             columns: [
        #                 %s
        #             ],
        #             type: "bar"
        #         },
        #     ''' % data_block
        # else:
        #     data_section = '''
        #         data: {
        #             x: "x",
        #             url: "%s",
        #             type: "line"
        #        },''' % self.data_url
        footer_scripts = """
        <script type="text/javascript">
            var chart = bb.generate({
                data: {
                    columns: [
                        %s
                    ],
                    type: "bar",
                },
                grid: {
                    x: {
                        show: false
                    },
                    y: {
                        show: true
                    }
                },
                bar: {
                    width: {
                        ratio: 0.5
                    }
                },
                axis: {
                    x: {
                        type: "category",
                        tick: {
                            width: 60,
                            culling: {
                                max: 5
                            },
                            autorotate: false,
                        },
                        categories: [
                            %s
                        ]
                    },
                    y: {
                        padding: {
                            top: 10,
                            bottom: 10
                        },
                        tick: {
                            culling: {
                                max: 5
                            },
                        },
                    },
                },
                legend: {
                    show: false
                },
                bindto: "#%s"
            });
        </script>
        """ % ( data_block, self.categories_csv, self.css_id)
        # footer_scripts2 = '''
        #     <script type="text/javascript">
        #         var chart%d = bb.generate({
        #             %s
        #             grid: {
        #                 x: {
        #                     show: true
        #                 },
        #                 y: {
        #                     show: true
        #                 }
        #             },
        #             point: {
        #                 focus: {
        #                     only: true
        #                 }
        #             },
        #             axis: {
        #                 x: {
        #                     type: "timeseries",
        #                     tick: {
        #                         fit: false,
        #                         count: 10,
        #                         format: "%s"
        #                     }
        #                 },
        #                 "y": {
        #                     "label": {
        #                         "text": "%s",
        #                         "position": "outer-middle"
        #                     },
        #                 },
        #             },
        #             zoom: {
        #                 enabled: true,
        #                 type: "drag"
        #             },
        #             legend: {
        #                 show: %s
        #             },
        #             bindto: "#%s"
        #         });
        #     </script>
        # ''' % (self.chart_num, data_section, tick_format, self.y_axis_label, show_legend_str, self.css_id)
        #% (
        #    css_id,
        #    data_url,
        #    options_str
        #)
        css_links = self.get_css_links()
        head_scripts = self.get_head_scripts()

        return RenderResponse(
            html=html,
            header_js=head_scripts,
            footer_js=footer_scripts,
            css_links=css_links,
        )



    def get_css_links(self):
        css_url = url_for("statics_page.static_file", file='billboard.min.css')
        return "<link rel='stylesheet' href='%s'>" % css_url

    def get_head_scripts(self):
        s = []
        s.append("<script src='https://d3js.org/d3.v6.min.js'></script>")
        head_scripts_url = url_for("statics_page.static_file", file='billboard.min.js')
        s.append("<script src='%s'></script>" % head_scripts_url)
        return "\n".join(s)

    @classmethod
    def example(cls):
        # Create sample data for the bar chart
        data = {
            'Q1': [120, 150, 180, 200],
            'Q2': [140, 160, 190, 210],
            'Q3': [160, 170, 200, 220],
            'Q4': [180, 190, 210, 240]
        }
        
        # Create DataFrame with sample data
        df = pd.DataFrame(data, index=['Product A', 'Product B', 'Product C', 'Product D'])
        
        # Create the chart component with a unique chart number
        import random
        chart = cls(
            chart_num=random.randint(1000, 9999),
            y_axis_label="Sales (thousands)",
            df=df,
            columns=['Q1', 'Q2', 'Q3', 'Q4'],
            title_html="<h3>Quarterly Sales Report</h3>",
            subtitle_html="<p>Sales performance by product and quarter</p>",
            show_legend=True,
            height='400px'
        )
        
        return chart

#
#
# <script src="https://d3js.org/d3.v6.min.js"></script>
#
# <!-- Step 2) Load billboard.js with style -->
# <script src="$YOUR_PATH/billboard.js"></script>
#
# <!-- Load with base style -->
# <link rel="stylesheet" href="$YOUR_PATH/billboard.css">

