from ..basecomponents import Component
from ..renderresponse import RenderResponse


class ModalComponent(Component):
    def __init__(
        self, css_id, title="Modal Title", body="Modal Body", footer="Modal Footer"
    ):
        self.css_id = css_id
        self.title = title
        self.body = body
        self.footer = footer

    def render(self):
        html = f"""
            <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                <h5 class="modal-title">{self.title}</h5>
                </div>
                <div class="modal-body">
                <p>{self.body}</p>
                </div>
                <div class="modal-footer">
                {self.footer}
                </div>
            </div>
            </div>
        """
        return RenderResponse(html=html)
    
    @classmethod
    def example(cls):
        return cls(
            css_id="example-modal",
            title="Example Modal",
            body="This is an example modal component with some sample content.",
            footer="<button type='button' class='btn btn-primary'>Save Changes</button>"
        )
