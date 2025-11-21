from flask import url_for
from .htmlcomponent import HTMLComponent
from ..basecomponents import Component
import json




class BlogPostComponent(Component):

    def __init__(self, slug, post):
        self.slug = slug
        self.post = post
        #self.img_src = img_src

    def render_section(self, section, show_heading=True):
        parts = []
        paragraph_style = "line-height: 1.6em;"
        print("Section ", json.dumps(section, indent=4))
        if show_heading:
            heading = section["heading"]
            text = section.get('text', '')
            heading_html = "<h2 style='font-size: 1.5rem;'>%s</h2>" % heading
            parts.append(heading_html)
            parts.append(f"<p style='{paragraph_style}'>{text}</p>")
        subsections = section["subsections"]
        for subsection in subsections:
            print("Subsection ", json.dumps(subsection, indent=4))

            heading = subsection["sub_heading"]
            text = subsection.get('text', '')
            heading_html = "<h3 style='font-size: 1.2rem;'>%s</h3>" % heading
            parts.append(heading_html)
            parts.append(f"<p style='{paragraph_style}'>{text}</p>")

            # for paragraph in paragraphs:
            #     sub_heading = paragraph["sub_heading"]
            #     sub_heading_html = "<h3 style='font-size: 1.2rem;'>%s</h3>" % sub_heading
            #     parts.append(sub_heading_html)
            #     parts.append("<p style='line-height: 1.6em;'>%s</p>" % paragraph["paragraph"])
        return "\n".join(parts)
    
    def render_section_v3(self, section, show_heading=True):
        parts = []
        paragraph_style = "line-height: 1.6em;"
        print("Section ", json.dumps(section, indent=4))
        # if show_heading:
        heading = section["title"]
        #     text = section.get('text', '')
        heading_html = "<h2 style='font-size: 1.5rem;'>%s</h2>" % heading
        parts.append(heading_html)
        #     parts.append(f"<p style='{paragraph_style}'>{text}</p>")
        subsections = section["subsections"]
        for subsection in subsections:
            print("Subsection ", json.dumps(subsection, indent=4))

            heading = subsection["sub_heading"]
            text = subsection.get('html', '')
            heading_html = "<h3 style='font-size: 1.2rem;'>%s</h3>" % heading
            parts.append(heading_html)
            parts.append(f"<p style='{paragraph_style}'>{text}</p>")

            # for paragraph in paragraphs:
            #     sub_heading = paragraph["sub_heading"]
            #     sub_heading_html = "<h3 style='font-size: 1.2rem;'>%s</h3>" % sub_heading
            #     parts.append(sub_heading_html)
            #     parts.append("<p style='line-height: 1.6em;'>%s</p>" % paragraph["paragraph"])
        return "\n".join(parts)
    
    def render_post_v3(self, article_dict):

        print("Render Post")
        print(json.dumps(article_dict, indent=4))
        
        parts = []

        headline = article_dict["title"]
        headline_html = "<h1>%s</h1>" % headline
        parts.append(headline_html)

        parts.append("<p><b>%s</b></p>" % article_dict["date"])
        sections = article_dict["sections"]

        idx = 0
        for section in sections:
            if idx == 0:
                show_heading = False
            else:
                show_heading = True
            html = self.render_section_v3(section, show_heading)
            parts.append(html)
            idx += 1

        return "\n".join(parts)
    

    def render_post(self, article_dict):

        print("Render Post")
        print(json.dumps(article_dict, indent=4))

        format = article_dict["format"]
        if format == "v3":
            return self.render_post_v3(article_dict)

        parts = []

        headline = article_dict["title"]
        headline_html = "<h1>%s</h1>" % headline
        parts.append(headline_html)

        parts.append("<p><b>%s</b></p>" % article_dict["date"])
        sections = article_dict["sections"]

        idx = 0
        for section in sections:
            if idx == 0:
                show_heading = False
            else:
                show_heading = True
            html = self.render_section(section, show_heading)
            parts.append(html)
            idx += 1

        return "\n".join(parts)
    

    def render(self):

        #date_str = self.post["date"].strftime("%B %d, %Y")
        img_src = self.post["img_src"]
        if img_src is not None:
            img_src_html = f"<img src='{img_src}' class='img-fluid'/>"
        else:
            img_src_html = ""

        body = self.render_post(self.post)  

        html = f"""
            <div class="blog-post mb-4" style='line-height: 2.1em; width:95%; margin: 0 auto;'>
                {img_src_html}
                {body}
            </div>
        """
        return HTMLComponent(html).render()
    
    @classmethod
    def example(cls):
        from datetime import datetime
        post = {
            "img_src": "/statics/images/test2.jpg",
            "format": "v3",
            "title": "Sample Blog Post",
            "date": "2024-01-15",
            "sections": [
                {
                    "title": "Introduction",
                    "subsections": [
                        {
                            "sub_heading": "Getting Started",
                            "text": "This is a sample blog post component that demonstrates how to display blog content with sections and subsections."
                        }
                    ]
                },
                {
                    "title": "Main Content",
                    "subsections": [
                        {
                            "sub_heading": "Key Points",
                            "text": "Here are some key points about the topic being discussed in this blog post."
                        }
                    ]
                }
            ]
        }
        return cls(slug="sample-blog-post", post=post)

