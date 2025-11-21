from flask import url_for
from .htmlcomponent import HTMLComponent
from ..basecomponents import Component


class BlogPostSummaryComponent(Component):

    def __init__(self, slug, post_row, summary_only=False, title_only=False):
        self.slug = slug
        self.post_row = post_row
        self.summary_only = summary_only
        self.title_only = title_only

    def render(self):
        date_str = self.post_row["date"].strftime("%B %d, %Y")
        if "img_src" in self.post_row:
            img_src = self.post_row["img_src"]
        else:
            img_src = None

        post_url = f"/blog/{self.slug}"  # Use simple URL instead of url_for
        if img_src is not None:
            img_src_html = f"<a href='{post_url}'><img src='{img_src}' class='img-fluid'/></a>"
        else:
            img_src_html = ""

        read_more_button = ""
        date_html = ""
        if self.title_only:
            body = ""
        else:
            if self.summary_only:
                body = self.post_row["intro"]
                parts = body.split(" ")
                parts = parts[:40]
                body = " ".join(parts) + " ..."
            else:
                body = self.render_post(self.post_row)  
                
            if self.summary_only:
                read_more_button = f"""<a href="{post_url}" class="btn btn-secondary btn-sm">Read More</a>"""

            date_html = f"<p style='font-size: 0.95rem;'>{date_str}</p>"

        html = f"""
            <div class="blog-post mb-4" style='line-height: 2.1em;  width:95%; margin: 0 auto;'>
                {img_src_html}
                <h2 style="font-size: 1.4rem;"><a href="{post_url}">{self.post_row['title']}</a></h2>
                {date_html}
                <p style="text-align: justify; line-height: 1.6em;">{body}</p>
                {read_more_button}
            </div>
        """
        return HTMLComponent(html).render()
    
    @classmethod
    def example(cls):
        from datetime import datetime
        post_row = {
            "title": "Sample Blog Post Summary",
            "date": datetime.now(),
            "img_src": "/statics/images/test2.jpg",
            "intro": "This is a sample blog post summary component that shows a preview of a blog post with title, date, image, and introductory text. It demonstrates how blog post summaries are displayed in lists or grids."
        }
        return cls(slug="sample-blog-post", post_row=post_row, summary_only=True)
