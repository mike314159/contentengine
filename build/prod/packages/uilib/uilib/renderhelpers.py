import os
import random
import pandas as pd
import datetime

from uilib import dftemplate as dft

# def render_tmpl(template_dir, fn, attrs):
#     fn = os.path.join(template_dir, fn)
#     if not os.path.exists(fn):
#         print("ERROR: render_tmpl(), path %s does not exist" % fn)
#         return ""
#     with open(fn, "r") as f:
#         html = f.read().replace("\n", "")
#         for key in attrs.keys():
#             value = attrs[key]
#             tkey = "{%s}" % key
#             html = html.replace(tkey, value)
#     return html
#
#
# def col_label_formatter(label):
#     return label.replace(".", "<br>.")
#


# def render_df(title, df, css_id, show_index=True, show_search=True):
#     tmpl = dft.DFTemplate()
#     colors_df = None
#     col_info_df = tmpl.build_col_info_df(df, col_label_formatter=col_label_formatter)
#     if title is not None:
#         title = "<p class='table_title'>%s</p>" % title
#     (html, js) = tmpl.render(
#         title,
#         css_id,
#         df,
#         col_info_df,
#         colors_df,
#         show_search,
#         show_idx=show_index
#     )
#     return (html, js)

def make_clickable(name, url):
    return '<a href="{}">{}</a>'.format(url, name)

def add_button_link(name, url):
    return f'''
        <a href="{url}">
            <button type="button" class="btn btn-secondary btn-sm">{name}</button>
        </a>
    '''
    #return '<a href="{}">{}</a>'.format(url, name)


def get_button_link_html(label, url, button_type="secondary", button_size="sm", active=False, css_style=""):
    if active:
        active_str = 'active'
    else:
        active_str = ''
    return f'''
        <a href="{url}">
            <button type="button" class="btn btn-{button_type} btn-{button_size} {active_str}" style="{css_style}">{label}</button>
        </a>
    '''

def add_df_link(df, label_column, url_column, destination_column):
    for idx, row in df.iterrows():
        label_value = row.get(label_column)
        url_value = row.get(url_column)
        if label_value is None or url_value is None:
            continue
        if destination_column in df.columns:
            df.at[idx, destination_column] = make_clickable(label_value, url_value)


def get_random_df(length=20, num_cols=3, min_value=-10, max_value=10):
    df = pd.DataFrame()
    #dt = datetime.datetime.now()
    z = random.randint(-20, 0)
    start_dt =  datetime.datetime.now() - datetime.timedelta(days=z)

    for i in range(1, num_cols+1):
        dt = start_dt
        a = random.randint(min_value, max_value)
        col_name = "value%s" % i
        #b = random.randint(-10, 10)
        #c = random.randint(-10, 10)
        for j in range(1, length):
            i = dt.strftime("%Y-%m-%d")
            a += random.randint(-10, 10)
            #b += random.randint(-10, 10)
            #c += random.randint(-10, 10)
            df.at[i,col_name] = a
            #df.at[i, "value2"] = b
            #df.at[i, "value3"] = c
            dt = dt - datetime.timedelta(days=1)
    return df

def get_htmx_attrs(get_url=None, post_url=None, target=None, swap='innerHTML', trigger='click'):
    # html = '''                <button 
    #             class="btn btn-primary"
    #             hx-get="%s" 
    #             hx-target="%s" 
    #             hx-swap="innerHTML" 
    #             hx-trigger="click" 
    #             data-bs-toggle="modal" 
    #             data-bs-target="%s" 
    #             hx-swap="innerHTML">Add</button>
    #     ''' % (url, target_css_id, target_css_id)
    
    c = []
    if get_url is not None:
        c.append("hx-get='%s'" % get_url)
    if post_url is not None:
        c.append("hx-post='%s'" % post_url)
    if target is not None:
        c.append("hx-target='%s'" % target)
    if swap is not None:
        c.append("hx-swap='%s'" % swap)
    if trigger is not None:
        c.append("hx-trigger='%s'" % trigger)

    return " ".join(c)
    

def generate_sitemap(domain, paths):
    # Get current time in UTC
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    lastmod_today = now_utc.isoformat()

    today = now_utc.replace(minute=0, second=0, microsecond=0).isoformat()

    # Get first day of the current month
    first_day_of_month = now_utc.replace(
        day=1, minute=0, second=0, microsecond=0
    ).isoformat()

    # Start the XML string
    sitemap = """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
    """

    for path in paths:
        loc = f"https://{domain}{path}"
        if path == "/":
            lastmod = today
            priority = "1.00"
        else:
            lastmod = first_day_of_month
            priority = "0.80"

        sitemap += f"""<url>
            <loc>{loc}</loc>
            <lastmod>{lastmod}</lastmod>
            <priority>{priority}</priority>
            </url>
        """
    sitemap += "</urlset>"
    return sitemap
