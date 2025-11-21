from ..basecomponents import Component
from ..renderresponse import RenderResponse


class PrettyDataframeTable(Component):

    def __init__(self, name, df, cols):
        super().__init__()
        self.df = df
        self.cols = cols

    """
    
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">First</th>
      <th scope="col">Last</th>
      <th scope="col">Handle</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td>Mark</td>
      <td>Otto</td>
      <td>@mdo</td>
    </tr>
    <tr>
      <th scope="row">2</th>
      <td>Jacob</td>
      <td>Thornton</td>
      <td>@fat</td>
    </tr>
    <tr>
      <th scope="row">3</th>
      <td colspan="2">Larry the Bird</td>
      <td>@twitter</td>
    </tr>
  </tbody>
</table>
    """

    def render(self):

        h = []
        h.append("<table class='table'>")

        # Header
        h.append("<thead>")
        h.append("<tr>")
        for col in self.cols:
            h.append("<th scope='col'>%s</th>" % col)
        h.append("</tr>")
        h.append("</thead>")

        # Body
        h.append("<tbody>")

        for idx, row in self.df.iterrows():
            h.append("<tr>")
            print("Row ", idx, " ", row)
            for col in self.cols:
                h.append("<td>%s</td>" % row[col])
            h.append("</tr>")

        h.append("</tbody>")

        h.append("</table>")
        html = "".join(h)
        js = ""
        return RenderResponse(html=html, footer_js=js)
    
    @classmethod
    def example(cls):
        import pandas as pd
        df = pd.DataFrame({
            'Name': ['John', 'Jane', 'Bob', 'Alice'],
            'Age': [25, 30, 35, 28],
            'City': ['New York', 'Los Angeles', 'Chicago', 'Boston']
        })
        return cls(
            name="sample_table",
            df=df,
            cols=['Name', 'Age', 'City']
        )
