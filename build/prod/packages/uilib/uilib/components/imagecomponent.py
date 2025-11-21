from ..basecomponents import Component
from ..renderresponse import RenderResponse
from flask import current_app


class ImageComponent(Component):
    def __init__(self, src, sub_title=None, width_px=None, url=None, padding='3px'):
        self.src = src
        self.sub_title = sub_title
        self.width_px = width_px
        self.url = url
        self.padding = padding

    def render(self):
        # Get the static base directory from SITE_CONFIG
        try:
            site_config = current_app.config['SITE_CONFIG']
            ui_lib_statics_base_dir = site_config.get_uilib_statics_base_dir()
            # Convert the src to use the proper static directory
            if self.src.startswith('/statics/'):
                # Replace /statics/ with the actual static directory path
                static_path = self.src.replace('/statics/', '')
                full_src = f"/statics/{static_path}"
            else:
                full_src = self.src
        except:
            # Fallback to original src if SITE_CONFIG is not available
            full_src = self.src
            
        padding_html = f"style='padding: {self.padding};'" if self.padding else ""
        if self.width_px is None:
            img_html = "<img src='%s' class='img-fluid' %s/>" % (full_src, padding_html)
        else:
            img_html = "<img src='%s' class='img-fluid' width='%dpx' %s/>" % (
                full_src,
                self.width_px,
                padding_html,
            )

        if self.sub_title is not None:
            html = f'''
            <div>
                {img_html}
                <div class="text-center">{self.sub_title}</div>
            </div>
            '''
        else:
            html = img_html

        if self.url is not None:
            html = "<a href='%s'>%s</a>" % (self.url, html)
        return RenderResponse(html=html)
    
    @classmethod
    def example(cls):
        return cls(
            src="/statics/images/test.jpeg",
            sub_title="Sample image with subtitle",
            width_px=300
        )
