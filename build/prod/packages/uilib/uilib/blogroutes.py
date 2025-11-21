from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory,
    url_for,
    make_response,
    redirect,
    flash,
    session,
    request,
    Blueprint,
    current_app,
)
import os

from uilib.components import (
    BlogPostComponent,
    BlogPostSummaryComponent,
    HTMLComponent,
    Container,
    BreadCrumbComponent,
    ComponentStack,
)
from uilib.blog import Blog

blog_blp = Blueprint("blog", __name__)

import random


def get_blog_routes():

    site_config = current_app.config["SITE_CONFIG"]
    blog = Blog(article_dir=site_config.get_blog_articles_dir())
    routes = []
    routes.append(url_for("blog.blog_home_page"))
    blog_articles_df = blog.get_blog_posts_df()
    for slug, row in blog_articles_df.iterrows():
        routes.append(url_for("blog.blog_post_page", slug=slug))

    return routes


# def get_upsell_component():
#     home_page_url = url_for("site_home_page")
#     html = f"""
#         <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; background-color: #e5e5e5;">
#             <div class="row justify-content-center">
#                 <div class="col-md-8 px-4 pt-3 text-center">
#                     <h2 class="hero-title mt-1">
#                         Master Math Fast! 
#                     </h2>
#                     <p class="mb-4 mt-3 hero-subtitle">
                        
#             MathStar provides customized practice and insights to make mastering math skills fast. See how it works.
            
#                     </p>
#                     <div class="justify-content-sm-center mt-4 mb-3">
#                         <a type="button" class="btn btn-primary btn-lg px-4 me-sm-3 active" href="{home_page_url}">Learn More</a>
                        
#                     </div>
#                     <div>
                        
#                     </div>
#                 </div>
#             </div>
#         </div>
#     """
#     return HTMLComponent(html)


@blog_blp.route("/images/<article_slug>/image.jpg")
def blog_image_serve_page(article_slug):
    site_config = current_app.config["SITE_CONFIG"]
    blog_dir = site_config.get_blog_articles_dir()
    article_dir = os.path.join(blog_dir, article_slug)
    return send_from_directory(article_dir, "image.jpg")


@blog_blp.route("/<slug>")
def blog_post_page(slug):

    analytics = current_app.config["ANALYTICS"]
    analytics.log_pageview(request, user_guid=None)

    body_comps = []

    site_config = current_app.config["SITE_CONFIG"]
    blog = Blog(article_dir=site_config.get_blog_articles_dir())

    post = blog.get_blog_post(slug)

    crumbs = [
        ("Home", url_for("site_home_page")),
        ("Blog", url_for("blog.blog_home_page")),
    ]
    breadcrumbs = BreadCrumbComponent(crumbs)
    body_comps.append(breadcrumbs)

    pp = BlogPostComponent(slug, post)
    body_comps.append(pp)

    comp = get_related_posts_component(current_slug=slug)
    body_comps.append(comp)

    page_renderer = current_app.config["PAGE_RENDERER"]
    return page_renderer.render_page(
        request=request,
        page_title="Article - " + post["title"],
        body_components=body_comps,
    )


def get_blog_object():
    site_config = current_app.config["SITE_CONFIG"]
    blog = Blog(article_dir=site_config.get_blog_articles_dir())
    return blog


def get_related_posts_component(current_slug, limit=4):
    blog = get_blog_object()
    posts_df = blog.get_blog_posts_df()

    stack = ComponentStack()
    pp = HTMLComponent("<h1 class='ml-5'>More Blog Posts</h1><br><br>")
    stack.add(pp)
    ctr = Container(cols=2, components=[], css_id="blog-posts", width=None)
    slugs = posts_df.index.tolist()
    slugs.remove(current_slug)
    slugs = random.sample(slugs, limit)
    for slug in slugs:
        row = posts_df.loc[slug]
        bp = BlogPostSummaryComponent(slug, row, title_only=True)
        ctr.add(bp)
    stack.add(ctr)
    return stack


@blog_blp.route("/")
def blog_home_page():

    analytics = current_app.config["ANALYTICS"]
    analytics.log_pageview(request, user_guid=None)

    body = []

    site_config = current_app.config["SITE_CONFIG"]
    blog = Blog(article_dir=site_config.get_blog_articles_dir())
    posts_df = blog.get_blog_posts_df()

    pp = HTMLComponent("<h1 class='ml-5'>Blog</h1><br><br>")
    body.append(pp)
    ctr = Container(cols=2, components=[], css_id="blog-posts", width=None)
    for slug, row in posts_df.iterrows():
        bp = BlogPostSummaryComponent(slug, row, summary_only=True)
        ctr.add(bp)

    body.append(ctr)

    # upsell_comp = get_upsell_component()
    # body.append(upsell_comp)

    page_renderer = current_app.config["PAGE_RENDERER"]
    return page_renderer.render_page(
        request=request,
        page_title="Portfolio Crunch - Blog",
        body_components=body,
    )
