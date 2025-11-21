from uilib.renderresponse import RenderResponse
from ..basecomponents import Component


class FeaturesComponent(Component):
    def __init__(self, title, desc, features, columns=3):
        """
        Initialize the FeaturesComponent with a title for the section and a list of features.
        Each feature in the list should be a dictionary with keys for title, description, and icon_href.

        :param title: The title of the features section.
        :param desc: The description text for the features section.
        :param features: A list of dictionaries, each representing a feature with title, description, and icon_href.
        :param columns: Number of columns (1, 2, or 3, defaults to 3)
        """
        self.title = title
        self.desc = desc
        self.features = features
        # Ensure columns is 1, 2, or 3
        self.columns = columns

    def render(self):
        # Set column classes based on the number of columns
        if self.columns == 1:
            col_classes = "row-cols-1 row-cols-sm-1 row-cols-md-1 row-cols-lg-1"
            text_align = "text-center"
        elif self.columns == 2:
            col_classes = "row-cols-1 row-cols-sm-1 row-cols-md-2 row-cols-lg-2"
            text_align = ""
        else:  # 3 columns
            col_classes = "row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-3"
            text_align = ""

        if self.desc is None:
            desc_html = ""
        else:
            desc_html = f'<p class="features-desc">{self.desc}</p>'

        html = f'<div id="features" class="container px-4 py-3" id="icon-grid">'
        html += f"""
            <div class="pricing-header p-3 pb-2 mx-auto text-center">
                <p class="features-title"><h1><a name="features">{self.title}</a></h1></p>
                {desc_html}
                </div>
        """

        html += f'<div class="row {col_classes} g-4 py-2">'

        # Loop through each feature and construct its HTML
        for feature in self.features:
            # Use text centering for single column layout
            desc_class = "text-center" if self.columns == 1 else "text-justify"
            
            # Adjust flex alignment for single column centering
            if self.columns == 1:
                flex_align = "d-flex align-items-center justify-content-center"
            else:
                flex_align = "d-flex align-items-start"
                
            html += f"""
      <div class="col {flex_align} py-3 px-3">
        <div class="{text_align}">
          <p class="mb-2 features-feature-title">{feature['title']}</p>
          <p class="mb-0 features-feature-desc {desc_class}">{feature['description']}</p>
        </div>
      </div>"""

        # Close the row and container div
        html += "</div></div>"
        return RenderResponse(html=html)

    @staticmethod
    def example():
        # Example usage of the FeaturesComponent
        example_features = [
            {
                "title": "Bootstrap",
                "description": "Explore the features of Bootstrap.",
                "icon_href": "#bootstrap",
            },
            {
                "title": "CPU Usage",
                "description": "Monitor CPU usage effectively.",
                "icon_href": "#cpu-fill",
            },
            {
                "title": "Calendar",
                "description": "Manage your schedules.",
                "icon_href": "#calendar3",
            },
            {
                "title": "Geolocation",
                "description": "Use geolocation for your apps.",
                "icon_href": "#geo-fill",
            },
            {
                "title": "Tools",
                "description": "Access a variety of tools.",
                "icon_href": "#tools",
            },
        ]
        example_component = FeaturesComponent(
            title="Features",
            desc="Quickly build an effective pricing table for your potential customers with this Bootstrap example. It's built with default Bootstrap components and utilities with little customization.",
            features=example_features,
            columns=3  # You can specify 1, 2, or 3 here
        )
        return example_component




