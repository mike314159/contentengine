from ..basecomponents import Component
from ..renderresponse import RenderResponse


class FileUploadComponent(Component):

    def __init__(self, upload_url):
        self.upload_url = upload_url

    def _get_js(self):
        js = (
            """
         <script>
function _(el) {
  return document.getElementById(el);
}

function uploadFile() {
  var file = _("file").files[0];
  // alert(file.name+" | "+file.size+" | "+file.type);
  var formdata = new FormData();
  formdata.append("file", file);
  var ajax = new XMLHttpRequest();
  ajax.upload.addEventListener("progress", progressHandler, false);
  ajax.addEventListener("load", completeHandler, false);
  ajax.addEventListener("error", errorHandler, false);
  ajax.addEventListener("abort", abortHandler, false);
  ajax.open("POST", "%s"); 
  //use file_upload_parser.php from above url
  ajax.send(formdata);
}

function progressHandler(event) {
  _("loaded_n_total").innerHTML = "Uploaded " + event.loaded + " bytes of " + event.total;
  var percent = (event.loaded / event.total) * 100;
  _("progressBar").value = Math.round(percent);
  _("status").innerHTML = Math.round(percent) + "pct uploaded... please wait";
}

function completeHandler(event) {
  _("status").innerHTML = event.target.responseText;
  _("progressBar").value = 0; //wil clear progress bar after successful upload
}

function errorHandler(event) {
  _("status").innerHTML = "Upload Failed";
}

function abortHandler(event) {
  _("status").innerHTML = "Upload Aborted";
}
</script>
        """
            % self.upload_url
        )
        return js

    def render(self):
        # html = "<div id='%s'></div>" % (self.css_id)

        html = """
<form id="upload_form" enctype="multipart/form-data" method="post">
  <input type="file" name="file" id="file" onchange="uploadFile()"><br>
  <progress id="progressBar" value="0" max="100" style="width:300px;"></progress>
  <h3 id="status"></h3>
  <p id="loaded_n_total"></p>
</form>
        """
        js = self._get_js()
        return RenderResponse(html=html, footer_js=js)
    
    @classmethod
    def example(cls):
        return cls(upload_url="/upload")
