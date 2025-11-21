from uilib.basecomponents import Component
from uilib.dftemplate import DFTemplate
from uilib.genericdataframetablecellformatter import GenericDataframeTableCellFormatter

class DataframeTable(Component):
    def __init__(
        self,
        df,
        css_id,
        title=None,
        sub_title=None,
        show_index=False,
        truncate_rows=None,
        show_search=True,
        add_checkboxes=False,
        button_label=None,
        show_columns=None,
        cell_styler=None,
        cell_value_formatter=None,
        view_all_button_label="View All",
        view_all_button_url=None,
        column_headers_replace_underscores=True,
        # an alternative simpler way to format columns
        cell_formats=None,
        selector_buttons=None,
        show_header=True,
    ):
        if df is not None:
            self.df = df.copy()
        else:
            self.df = df
            
        self.css_id = css_id
        self.title = title
        self.sub_title = sub_title
        self.show_index = show_index
        self.show_search = show_search
        self.show_header = show_header
        self.add_checkboxes = add_checkboxes
        self.button_label = button_label
        self.msg = None
        if truncate_rows is not None:
            (self.df, self.msg) = DataframeTable._truncate_df(self.df, truncate_rows)
        self.show_columns = show_columns
        self.view_all_button_label = view_all_button_label
        self.view_all_button_url = view_all_button_url

        self.cell_styler = cell_styler
        self.column_headers_replace_underscores = column_headers_replace_underscores

        #if cell_value_formatter is None and column_formats is not None:
        #    cell_value_formatter = GenericDataframeTableCellFormatter(column_formats)

        self.cell_value_formatter = cell_value_formatter
        self.cell_formats = cell_formats
        self.selector_buttons = selector_buttons
        
    def _truncate_df(df, row_limit):
        if df is None:
            return (df, "Empty Dataframe")
        if len(df.index) > row_limit:
            row_count = len(df.index)
            df = df.sample(n=row_limit)
            msg = (
                "<br>WARNING: Displaying only %d random rows. %d rows in original dataset."
                % (row_limit, row_count)
            )
            return (df, msg)
        else:
            return (df, None)

    def render(self):
        tmpl = DFTemplate(add_checkboxes=False)
        render_response = tmpl.render(
            df=self.df,
            css_id=self.css_id,
            title=self.title,
            sub_title=self.sub_title,
            show_search=self.show_search,
            show_index=self.show_index,
            striped=True,
            cell_styler=self.cell_styler,
            cell_value_formatter=self.cell_value_formatter,
            cell_formats=self.cell_formats,
            show_columns=self.show_columns,
            view_all_button_label=self.view_all_button_label,
            view_all_button_url=self.view_all_button_url,
            column_headers_replace_underscores=self.column_headers_replace_underscores,
            selector_buttons=self.selector_buttons,
            show_header=self.show_header,
        )
        return render_response

    def get_global_js():
        return DFTemplate.get_global_js()

