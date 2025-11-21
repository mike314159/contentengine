
# https://tomik23.github.io/autocomplete/

import json
from flask import (
    url_for
)
from ..basecomponents import Component

class Autocomplete(Component):

    def __init__(self):
        pass
        # self.options = {
        # }

    # def _set_option(self, k, v):
    #     self.options[k] = v
    #

    def render_basic(self, search_data_url):

        html = '''
            <div class="auto-search-wrapper">
                <input type="text" class='form-control' id="basic" placeholder="type a few characters">
            </div>
        '''

        js = '''
        <script type="text/javascript">
            new Autocomplete("basic", {
              onSearch: ({ currentValue }) => {
                const api = `%s?search=${encodeURI(
                  currentValue
                )}`;
                return new Promise((resolve) => {
                  fetch(api)
                    .then((response) => response.json())
                    .then((data) => {
                      resolve(data);
                    })
                    .catch((error) => {
                      console.error(error);
                    });
                });
              },
              onResults: ({ matches }) =>
                matches.map((el) => `<li>${el.label}</li>`).join(""),
            });
        </script>
        ''' % search_data_url
        return (html, js)

    def render(self, search_data_url):

        # Multiple entries
        html = '''
            <div class="auto-search-wrapper max-height loupe">
                <input type="text" class='form-control' id="multiple-choices" placeholder="type w">
            </div>
        '''

        js = '''
            <script type="text/javascript">               
                // array initialization
                let secondArray = [];

                new Autocomplete("multiple-choices", {
                    onSearch: ({ element }) => {             
                        const lastElement = element.value.split(",").pop().trim();
                        // if the last item is 0 then we don't do a search
                        if (lastElement.length === 0) return; 
                        const api = `%s?search=${encodeURI(lastElement)}`;
                    return new Promise((resolve) => {
                        fetch(api)
                        .then((response) => response.json())
                        .then((data) => {
                            resolve(data);
                    })
                    .catch((error) => {
                      console.error(error);
                    });
                });
              },
        
  onResults: ({ matches }) =>
    matches.map((el) => `<li class='loupe'>${el.label}</li>`).join(""),

  onOpened: ({ element, results }) => {
    // type - two values 'results' and 'showItems',
    // 'resutls' first rendering of the results
    // 'showItems' only showing the results when clicking on the input field
    // resultList all results rendered containing ul and li
    // input - root input

    // get the data from the input field and divide by the
    // decimal point, then remove the empty last element
    const currentValue = element.value
      .split(", ")
      .splice(0, element.value.length - 1);

    // leave in the array only those elements that are in the input field
    secondArray = secondArray.filter((el) => currentValue.includes(el));

    // check if the table 'multipleArr' contains selected elements from
    // the input field, if so we add the 'selected' class to the 'li' element,
    // if not, remove the 'selected' class from the li element
    [].slice.call(results.children).map((item) => {
      item.classList[secondArray.includes(item.textContent) ? "add" : "remove"](
        "selected"
      );
    });
  },

  onSubmit: ({ index, element, object, results }) => {
    if (secondArray.includes(element.value)) {
      return;
    }

    console.log("index: ", index, "object: ", object, "results: ", results);

    // each click on the li element adds data to the array
    secondArray.push(element.value.trim());

    // check if the table includes selected items from
    // the list, if so, add the 'selected' class
    [].slice.call(results.children).map((item) => {
      if (secondArray.includes(item.textContent)) {
        item.classList.add("selected");
      }
    });

    // add the elements from the array separated by commas
    // to the 'input' field, also add a comma to the last element
    element.value = `${secondArray.join(", ")}${
      secondArray > 2 ? secondArray.pop()[secondArray.length - 1] : ", "
    }`;

    // after selecting an item, set the
    // focus to the input field
    element.focus();
  },

  onReset: (element) => {
    // after clicking the 'x' button,
    // clear the table
    secondArray = [];
  },
});

        </script>
        ''' % search_data_url
        return (html, js)

    def get_css_links(self):
        css_url = url_for("statics_page.static_file", file='autocomplete.min.css')
        return "<link rel='stylesheet' href='%s'>" % css_url

    def get_head_scripts(self):
        head_scripts_url = url_for("statics_page.static_file", file='autocomplete.min.js')
        return "<script src='%s'></script>" % head_scripts_url
    
    def render(self):
        # Use the basic render method for the example
        html, js = self.render_basic("/api/search")
        from ..renderresponse import RenderResponse
        return RenderResponse(html=html, footer_js=js)
    
    @classmethod
    def example(cls):
        return cls()
