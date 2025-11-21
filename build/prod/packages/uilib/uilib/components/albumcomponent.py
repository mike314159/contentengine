from ..renderresponse import RenderResponse
from ..basecomponents import Component


class AlbumComponent(Component):

    def __init__(
        self, content, empty_message="No items to display"
    ):  
        self.content = content
        self.empty_message = empty_message

    # def _get_column_html(self, card_text, view_button_label, edit_button_label, time):
    #     template = f'''
    #     <div class="col">
    #         <div class="card shadow-sm">
    #             <div class="card-body">
    #                 <p class="card-text">{card_text}</p>
    #                 <div class="d-flex justify-content-between align-items-center">
    #                     <div class="btn-group">
    #                         <button type="button" class="btn btn-sm btn-outline-secondary">{view_button_label}</button>
    #                         <button type="button" class="btn btn-sm btn-outline-secondary">{edit_button_label}</button>
    #                     </div>
    #                     <small class="text-body-secondary">{time}</small>
    #                 </div>
    #             </div>
    #         </div>
    #     </div>
    #     '''
    #     return template

    def generate_html(self, content):

        if len(content["cols"]) == 0:
            empty_html = f"<p><b>{self.empty_message}</b></p>"
        else:
            empty_html = ""

        container_template = """
            <div class="pb-md-4 mx-auto">
                <h2>{title}</h2>
                {description_html}
                <div class="row row-cols-1 row-cols-sm-2 row-cols-md-2 g-3">
                    {cols_html}
                    {empty_html}
                </div>
            </div>
        """

        # row_template = '''
        #     <div class="pb-md-4 mx-auto">
        #         <h2 class="">{row_title}</h2>
        #         <p class="fs-5 text-muted">{row_description}</p>
        #     </div>
        #     <div class="row row-cols-1 row-cols-sm-2 row-cols-md-2 g-3">
        #         {cols_html}
        #     </div>
        # '''

        col_template = """
            <div class="col">
                <div class="card shadow-sm">
                    <div class="card-body">
                        <span style="font-size: 0.85rem; color: gray;">{category}</span>
                        <h5 style="margin-top: 5px;">{title}</h5>
                        {subtitle_html}
                        <p class="card-text">{card_text}</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="btn-group">
                                <a href="{button_url}" class="btn btn-sm btn-outline-primary {button_active}">{button_label}</a>
                            </div>
                            <span class="badge bg-secondary">{right_text}</span>
                        </div>
                    </div>
                </div>
            </div>
        """

        # for row in content['rows']:
        #     html_output += row_template.format(
        #         row_title=row['title:'],
        #         row_description=row['description']
        #     )

        cols_html = ""
        for col in content["cols"]:
            button_active = "active" if col["button"]["active"] else ""
            subtitle_html = f'<p style="font-size: 0.9rem;">{col.get("subtitle", "")}</p>' if col.get("subtitle") else ""
            cols_html += col_template.format(
                category=col["category"].upper(),
                title=col["title"],
                subtitle_html=subtitle_html,
                card_text=col["text"],
                button_label=col["button"]["label"],
                button_url=col["button"]["url"],
                button_active=button_active,
                right_text=col["right_text"],
            )

        # row_html = row_template.format(
        #             row_title=row['title'],
        #             row_description=row['description']
        #             cols_html=cols_html
        #         )

        description = content.get("description", None)
        if description is None:
            description_html = ""
        else:
            description_html = f"<p>{content['description']}</p>" if content.get('description') else ""

        html = container_template.format(
            title=content["title"],
            description_html=description_html,
            cols_html=cols_html,
            empty_html=empty_html,
        )
        return html

    def render(self):

        # self.title = 'Work On These Skills'
        # self.description = 'Quickly build an effective pricing table for your potential customers with this Bootstrap example. It's built with default Bootstrap components and utilities with little customization.'

        # #test_col = self._get_column_html('Card Text', 'View', 'Edit', '9 mins')

        # content = {

        #     'title': self.title,
        #     'description': self.description,

        #     'rows': [
        #         {
        #             'title:': 'Recommended New Skills',
        #             'description': 'Description Row',
        #             'cols': [
        #                 {
        #                     'title': 'Col Title',
        #                     'text': 'Test Text',
        #                     'button': {
        #                         'label': 'View',
        #                         'url': '/view'
        #                     },
        #                     'right_text': '9 mins'
        #                 },
        #                 {
        #                     'title': 'Col Title',
        #                     'text': 'Test Text',
        #                     'button': {
        #                         'label': 'View',
        #                         'url': '/view'
        #                     },
        #                     'right_text': '9 mins'
        #                 },
        #                 {
        #                     'title': 'Col Title',
        #                     'text': 'Test Text',
        #                     'button': {
        #                         'label': 'View',
        #                         'url': '/view'
        #                     },
        #                     'right_text': '9 mins'
        #                 },
        #                 {
        #                     'title': 'Col Title',
        #                     'text': 'Test Text',
        #                     'button': {
        #                         'label': 'View',
        #                         'url': '/view'
        #                     },
        #                     'right_text': '9 mins'
        #                 },

        #             ]
        #         },
        #         {
        #             'title:': 'Improve Existing Skills',
        #             'description': 'Description Row',
        #             'cols': [
        #                 {
        #                     'title': 'Col Title',
        #                     'text': 'Test Text',
        #                     'button': {
        #                         'label': 'View',
        #                         'url': '/view'
        #                     },
        #                     'right_text': '9 mins'
        #                 },
        #                 {
        #                     'title': 'Col Title',
        #                     'text': 'Test Text',
        #                     'button': {
        #                         'label': 'View',
        #                         'url': '/view'
        #                     },
        #                     'right_text': '9 mins'
        #                 },
        #                 {
        #                     'title': 'Col Title',
        #                     'text': 'Test Text',
        #                     'button': {
        #                         'label': 'View',
        #                         'url': '/view'
        #                     },
        #                     'right_text': '9 mins'
        #                 },
        #                 {
        #                     'title': 'Col Title',
        #                     'text': 'Test Text',
        #                     'button': {
        #                         'label': 'View',
        #                         'url': '/view'
        #                     },
        #                     'right_text': '9 mins'
        #                 },

        #             ]
        #         }
        #     ]
        # }

        html = self.generate_html(self.content)
        return RenderResponse(html=html)
    
    @classmethod
    def example(cls):
        content = {
            "title": "Sample Album",
            "description": "This is a sample album component with some example content.",
            "cols": [
                {
                    "title": "Sample Item 1",
                    "text": "This is the first item in the album with some descriptive text.",
                    "category": "featured",
                    "button": {
                        "label": "View",
                        "url": "/view/1",
                        "active": False
                    },
                    "right_text": "5 mins"
                },
                {
                    "title": "Sample Item 2", 
                    "text": "This is the second item in the album with different content.",
                    "category": "standard",
                    "button": {
                        "label": "Edit",
                        "url": "/edit/2",
                        "active": False
                    },
                    "right_text": "10 mins"
                },
                {
                    "title": "Sample Item 3",
                    "text": "This is the third item showing how the album displays multiple items.",
                    "category": "premium",
                    "button": {
                        "label": "View",
                        "url": "/view/3",
                        "active": False
                    },
                    "right_text": "3 mins"
                }
            ]
        }
        return cls(content=content)
        # html = f'''
        #     <div class="container">

        #         <div class="pricing-header p-3 pb-md-4 mx-auto">
        #             <h1 class="">{self.title}</h1>
        #             <p class="fs-5 text-muted">{self.description}</p>
        #         </div>

        #         <div class="pricing-header p-3 pb-md-4 mx-auto">
        #             <h2 class="">{self.title}</h2>
        #             <p class="fs-5 text-muted">{self.description}</p>
        #         </div>

        #         <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3">
        # <div class="col">
        #     <div class="card shadow-sm">
        #         <div class="card-body">
        #             <p class="card-text">{card_text}</p>
        #             <div class="d-flex justify-content-between align-items-center">
        #                 <div class="btn-group">
        #                     <button type="button" class="btn btn-sm btn-outline-secondary">{view_button_label}</button>
        #                     <button type="button" class="btn btn-sm btn-outline-secondary">{edit_button_label}</button>
        #                 </div>
        #                 <small class="text-body-secondary">{time}</small>
        #             </div>
        #         </div>
        #     </div>
        # </div>
        #         <div class="col">
        #     <div class="card shadow-sm">
        #         <div class="card-body">
        #             <p class="card-text">{card_text}</p>
        #             <div class="d-flex justify-content-between align-items-center">
        #                 <div class="btn-group">
        #                     <button type="button" class="btn btn-sm btn-outline-secondary">{view_button_label}</button>
        #                     <button type="button" class="btn btn-sm btn-outline-secondary">{edit_button_label}</button>
        #                 </div>
        #                 <small class="text-body-secondary">{time}</small>
        #             </div>
        #         </div>
        #     </div>
        # </div>
        #                         </div>

        #     </div>
        #     '''
