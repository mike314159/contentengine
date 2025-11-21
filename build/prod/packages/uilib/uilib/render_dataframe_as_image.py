import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from uilib.cellvalueformatter import CellValueFormatter
from uilib.magnitudetablecellstyler import MagnitudeTableCellStyler



def render_dataframe_as_image(df, cell_styler, cell_value_formatter, fn, footnote=None):

    # These are the same values than 'columns'
    
    columns = df.columns
    rows = [r for r in columns]

    # Get some pastel shades for the colors
    column_colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))
    row_colors = ["#FFFFFF"] * len(df.index)

    # Plot bars and create text labels for the table
    cell_text = []

    # Take a look that data is extracted from the Pandas df
    for _, row in df.iterrows():
        formatted_row = [
            cell_value_formatter.format(col, row[col]) for col in columns
        ]
        cell_text.append(formatted_row)

    print(cell_text)
    #input("Press Enter to continue...")

    row_count = max(len(df.index), 1)
    row_height = 0.8
    header_height = 0.8
    footnote_height = 0.6 if footnote else 0
    fig_height = row_height * row_count + header_height + footnote_height
    fig = plt.figure(figsize=(6, fig_height), dpi=100)

    # Reverse colors and text labels to display the last value at the top.
    column_colors = column_colors[::-1]

    footnote_ratio = 0.2 if footnote else 0.05
    table_ax = fig.add_axes([0, footnote_ratio, 1, 1 - footnote_ratio])
    table_ax.axis('off')

    the_table = table_ax.table(
        cellText=cell_text,
        rowLabels=df.index,
        rowColours=row_colors,
        colLabels=columns,
        colColours=column_colors,
        loc='center',
    )
    the_table.scale(1.5, 5)

    the_table.auto_set_font_size(False)
    the_table.set_fontsize(28)

    fig.canvas.draw()
    the_table.auto_set_column_width(col=[-1])
    renderer = fig.canvas.get_renderer()
    text_padding = 0.01
    for (row, col), cell in the_table.get_celld().items():
        if col == -1:
            text_bbox = cell.get_text().get_window_extent(renderer=renderer)
            text_width = text_bbox.width / fig.dpi / fig.get_size_inches()[0]
            cell.set_width(text_width + text_padding)

    for (row, col), cell in the_table.get_celld().items():
        if col == -1 and row > 0:
            cell.get_text().set_ha("left")
            cell.PAD = 0.05
            cell.set_facecolor("#FFFFFF")
            continue
        if row == 0 and col >= 0:
            cell.set_facecolor("#EAEAEA")
            cell.get_text().set_fontweight("bold")
            continue
        if row <= 0 or col < 0:
            continue
        row_label = df.index[row - 1]
        col_label = columns[col]
        if (
            row_label in cell_styler.colors_df.index
            and col_label in cell_styler.colors_df.columns
        ):
            color = cell_styler.colors_df.at[row_label, col_label]
            if not pd.isna(color):
                cell.set_facecolor(color)

    if footnote:
        footnote_ax = fig.add_axes([0, 0, 1, footnote_ratio])
        footnote_ax.axis('off')
        footnote_ax.text(
            1.2,
            0.25,
            footnote,
            ha="right",
            va="center",
            fontsize=22,
            color="#555555",
        )

    # If you want to save the table to disk...
    plt.savefig(fn, bbox_inches='tight', pad_inches=0.1)

