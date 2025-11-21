import pandas as pd
#from uilib import formathelpers as fh

# Render a dataframe to a table


class DFTemplate:
    def __init__(self):
        pass

    def build_tmpl(css_id, header, body):
        tbl = (
            "<table id='%s' class='table table-striped table-bordered table-hover' cellspacing='0' width='100%s'>"
            % (css_id, "%")
        )
        tbl = "%s<thead>%s</thead>" % (tbl, header)
        tbl = "%s<tbody>%s</tbody>" % (tbl, body)
        tbl = "%s</table>" % tbl
        return tbl

    def build_col_info_df(df, col_label_formatter=None):
        idx = 0
        col_info_df = pd.DataFrame()
        if df is None:
            return col_info_df
        cols = df.columns
        print("Cols ", cols)
        for col in cols:
            if col_label_formatter is not None:
                label = col_label_formatter(col)
            else:
                label = col
            col_info_df.at[idx, "label"] = label
            col_info_df.at[idx, "key"] = col
            idx += 1
        return col_info_df

    def get_header(col_info_df, show_idx=True):
        header = ["<tr>"]
        if show_idx:
            header.append("<th scope='col'>index</th>")
        for idx, row in col_info_df.iterrows():
            if "label" in row:
                col_label = row["label"]
            else:
                if "key" in row:
                    col_label = row["key"]
                else:
                    col_label = idx
            header.append("<th scope='col'>%s</th>" % col_label)
        header.append("</tr>")
        return "".join(header)

    def get_body(df, col_info_df, show_idx=True, colors_df=None, value_formatter=None):

        # new_col_names = {}
        # for col in df.columns:
        #     new_col_names[col] = col.replace('.', "X")
        # #df.rename(columns=new_col_names, inplace=True)

        # for col in df.columns:
        #    df[col] = df[col].map(lambda x: '{0:.2f}'.format(x))

        print(col_info_df)
        rows = []
        if df is None:
            return "<tr></tr>"
        for ridx, row in df.iterrows():
            #print("Row Index ", ridx)
            r = ["<tr>"]
            if show_idx:
                #v = ', '.join(map(str, ridx))
                r.append("<td>%s</td>" % ridx)
            for cidx, info in col_info_df.iterrows():
                col_key = info["key"]
                if col_key in row:
                    if value_formatter is not None:
                        v = value_formatter(row[col_key])
                    else:
                        v = row[col_key]
                else:
                    v = "?"

                cell = None
                if colors_df is not None:
                    if col_key in colors_df.columns:
                        bgcolor = colors_df.get_value(ridx, col_key)
                        if bgcolor != "":
                            cell = "<td bgcolor='%s'>%s</td>" % (bgcolor, v)

                if cell is None:
                    cell = "<td>%s</td>" % v

                r.append(cell)
            r.append("</tr>")
            rows.append("".join(r))
        return "".join(rows)

    def get_ready_js(css_id, show_search):
        js = ["<script>"]
        js.append("$(document).ready(function() {")
        js.append("$('#%s').DataTable( {" % css_id)
        js.append('"aaSorting": [],')
        if show_search:
            search_str = "true"
        else:
            search_str = "false"

        js.append('"searching": %s,' % search_str)
        js.append('"paging": false,')
        js.append('"info": false')
        js.append("});")
        js.append("});")
        js.append("</script>")
        return "".join(js)



    def format_and_render(title, df, cols, css_id, show_search):
        (cols_df, fdf, colors_df) = DFTemplate.get_format_highlight_dfs(df, cols)
        (html, js) = DFTemplate.render(title, css_id, fdf, cols_df, colors_df, show_search)
        return (html, js)

    """
    Expecting cols to be in the format
        cols = {
        "symbol": {"o": 1,  "label": "Symbol", "f": fh.formatPassThru, "c": fh.formatNoColor},
        "name":   {"o": 2,  "label": "Name", "f": fh.formatPassThru, "c": fh.formatNoColor},
    """

    def get_format_highlight_dfs(df, cols):
        col_info_df = pd.DataFrame()
        fdf = pd.DataFrame()
        colors_df = pd.DataFrame()
        for col, info in cols.items():
            fmt_func = info["f"]
            fh.format_df_col(df, fdf, col, fmt_func)

            color_func = info["c"]
            fh.format_colors_df_col(df, colors_df, col, color_func)

            i = info["o"]
            col_info_df.set_value(i, "key", col)
            col_info_df.set_value(i, "label", info["label"])

        col_info_df.sort_index(ascending=True, inplace=True)
        return (col_info_df, fdf, colors_df)


    def render(
        title, css_id, df, col_info_df, colors_df, show_search=True, show_idx=True, value_formatter=None
    ):
        if title is not None:
            title = "<h3>%s</h3>" % title
        else:
            title = ""
        if df is None or len(df.index) == 0:
            return (title + "<br>" + "Empty", "")
        else:
            if col_info_df is None:
                col_info_df = DFTemplate.build_col_info_df(df)

            header = DFTemplate.get_header(col_info_df, show_idx)
            body = DFTemplate.get_body(df, col_info_df, show_idx, colors_df, value_formatter)
            js = DFTemplate.get_ready_js(css_id, show_search)
            table_html = DFTemplate.build_tmpl(css_id, header, body)
            html = title + "<br>" + table_html
            return (html, js)

    def render_df(title, df, css_id, show_index=True, show_search=True):
        colors_df = None
        col_info_df = DFTemplate.build_col_info_df(df, col_label_formatter=None)
        if title is not None:
            title = "<p class='table_title'>%s</p>" % title
        (html, js) = DFTemplate.render(
            title,
            css_id,
            df,
            col_info_df,
            colors_df,
            show_search,
            show_idx=show_index,
            value_formatter=None,
        )
        return (html, js)