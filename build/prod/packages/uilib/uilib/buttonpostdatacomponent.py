from ..basecomponents import Component
from ..renderresponse import RenderResponse


class ButtonPostDataComponent(Component):
    def __init__(self, label, post_url, redirect_url=None, data=None):
        self.post_url = post_url
        self.redirect_url = redirect_url
        self.data = data
        self.label = label
        self.button_css_id = "my-button"

    def _js(self):
        js = """
        <script>
            // select the button element
            const button = document.querySelector('#my-button');

            // attach a click event listener to the button
            button.addEventListener('click', () => {
            // create an object with the values to be submitted
            const formData = {
                name: 'John Doe',
                email: 'john@example.com',
                message: 'This is my message.'
            };

            // encode the form data as a URL-encoded string
            const encodedData = Object.keys(formData)
                .map((key) => encodeURIComponent(key) + '=' + encodeURIComponent(formData[key]))
                .join('&');

            // using fetch API to send the POST request
            fetch('%s', {
                method: 'POST',
                body: encodedData,
                headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
                }
            })
            .then(() => {
                // redirect to another page after the POST request is successful
                window.location.href = '%s';
            })
            .catch((error) => {
                console.error(error);
            });
            });
        </script>
        """ % (
            self.post_url,
            self.redirect_url,
        )
        return js

    def render(self):
        # html = "<a id='%s' class='btn btn-primary' href='%s' role='button'>%s</a>" % (self.button_css_id, self.url, self.label)
        html = "<button id='%s' class='btn btn-primary' type='button'>%s</button>" % (
            self.button_css_id,
            self.label,
        )
        js = self._js()
        return RenderResponse(html=html, footer_js=js)
