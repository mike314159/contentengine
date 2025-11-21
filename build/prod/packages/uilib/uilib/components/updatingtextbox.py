from ..basecomponents import Component
from ..renderresponse import RenderResponse


class UpdatingTextBox(Component):
    def __init__(self, css_id, url):
        self.url = url
        self.css_id = css_id

    def _get_js(self, url, element_id, refresh_interval_secs=2):
        js = """
            const textBox = document.getElementById(%s);
            function pollAPI() {
            fetch('%s')
                .then(response => response.json())
                .then(data => {
                textBox.value = data.result;
                setTimeout(pollAPI, %d); // call the function again after 2 seconds
                })
                .catch(error => console.error(error));
            }
            pollAPI(); // start polling the API
        """ % (
            element_id,
            url,
            refresh_interval_secs * 1000,
        )
        return js

    def render(self):
        html = "<div id='%s'></div>" % (self.css_id)
        js = self._get_js(self.url, element_id=self.css_id)
        return RenderResponse(html=html, footer_js=js)
    
    @classmethod
    def example(cls):
        return cls(
            css_id="updating-textbox-example",
            url="/api/status"
        )
