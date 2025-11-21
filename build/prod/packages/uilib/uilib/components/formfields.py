
from uilib.basecomponents import *
from uilib.renderhelpers import *
import json
from email_validator import validate_email, EmailNotValidError
import hashlib

class FormInputField:
    def __init__(self, name, label=None, help=None, required=False, disabled=False):
        self.form_css_id = None
        self.name = name
        self.required = required
        self.disabled = disabled
        self.label=label
        self.help_text=help
        self.value = None

        self.valid = True
        self.error_msg = None
        #print("Init Field: ", self.name, " is_valid: ", self.is_valid())

    def _set_value(self, value):
        self.value = value

    def set_error(self, error_msg):
        self.error_msg = error_msg
        self.valid = False

    def validate(self):
        self.valid, self.error_msg = self._validate()
        #print("Setting field name: ", self.name, " is_valid: ", self.is_valid())
        if self.error_msg is not None:
            #print(f"Field Invalid : {self.name} : {self.error_msg}")
            pass

    def is_valid(self):
        return self.valid

    def validate_field(self, request):
        if self.required:
            if self.value is None or self.value == "":
                self.valid, self.error_msg = (False, "Field is required")
                return self.valid
        return self.valid

    def get_is_invalid_class(self):
        #print("Field: ", self.name, " is_valid: ", self.is_valid())
        if not self.is_valid():
            return "is-invalid"
        else:
            return ""
        
    def is_required(self):
        return self.required

    def is_disabled(self):
        return self.disabled

    def min_value(self):
        return None
    
    def max_value(self):
        return None
    
    def disable(self):
        self.disabled = True
    
    # def wrap_label(self, html):
    #     if self.label is None:
    #         return html
        
    #     help = '''
    #         <br>
    #         <small class="form-text text-muted">%s
    #         </small>
    #     ''' % self.help_text
    #     h = []
    #     h.append("<div class='mb-3'>")
    #     h.append("<label for='%s' class='form-label'><b>%s</b></label>" % (self.name, self.label))
    #     #if self.help_text is not None:
    #     h.append(help)
    #     h.append(html)
    #     h.append("</div>")
    #     return "\n".join(h)

    def _field_help_tmpl(self, help_text, help_block_id):
        if help_text is None:
            return ""
        else:
            return f"""
                        <div id="{help_block_id}" class="form-text mb-1 mt-0">
                        {help_text}
                        </div>
                    """

    def _field_tmpl(self, field_html):


        if not self.is_valid():
            error_tmpl = f"""
                <div id="validationServerUsernameFeedback" class="invalid-feedback">
                    {self.error_msg}
                </div>
            """
        else:
            error_tmpl = ""

        help_block_id = "%s_help_block" % self.name
        help_block = self._field_help_tmpl(self.help_text, help_block_id)
        html = f"""
            <div class="mb-4">
                <label for="{id}" class="form-label fw-semibold mb-1" style="display: inline-block; text-align: left !important; width: auto;">{self.label}</label>
                {help_block}
                {field_html}
                {error_tmpl}
            </div>
        """
        return html
    



    
# class ButtonField(InputField):
#
#     def __init__(self, id, label):
#         super().__init__(id)
#         self.label = label
#
#     def render(self):
#         return  "<button type='button' class='btn btn-primary btn-smb>%s</button>" % self.label


# class DecimalField(FormInputField):
#     def __init__(self, id, value):
#         super().__init__(id)
#         self.value = value

#     def is_valid(self):
#         if self.value is None:
#             return (True, "")
#         try:
#             dec = decimal.Decimal(self.value)
#             return (True, "")
#         except (decimal.InvalidOperation, ValueError) as exc:
#             # raise ValueError(self.gettext("Not a valid decimal value.")) from exc
#             return (False, "Value '%s' is not a valid value" % self.value)

#     def render(self):
#         if self.value is None:
#             value = ""
#         else:
#             value = self.value

#         (valid, msg) = self.is_valid()
#         if valid:
#             invalid_class = ""
#         else:
#             invalid_class = "is-invalid"

#         style = "display: inline; width:25%;"
#         return (
#             "<input type='text' class='form-control %s' id='%s' name='%s' value='%s' style='%s'>"
#             % (invalid_class, self.id, self.id, value, style)
#         )


class FormTextField(FormInputField):


    # field type can also be password
    def __init__(self, name, label=None, help=None, width=None, required=False, disabled=False, placeholder=None, field_type='text'):
        super().__init__(name, label, help, required=required, disabled=disabled)
        self.width = width
        self.placeholder = placeholder
        self.field_type = field_type
        assert field_type in ['text', 'password', 'email']
        #print("Field Name: ", self.name, " is_required: ", self.required)

    def _validate(self):
        #print("INFO: Validating field ", self.name)
        if self.required:
            #print("INFO: Field is required ", self.name)
            if self.value is None or self.value == "":
                #print("INFO: Field is required but value is empty ", self.name)
                return (False, "Field is required")
        return (True, None)
    
    def validate_field(self, request):
        valid = super().validate_field(request)
        return valid


    def render(self):
        if self.value is None:
            value = ""
        else:
            value = self.value

        # width_map = {
        #     'small': 'width: 100px;',
        #     'medium': 'width: 100px;',
        #     'large': 'width: 100px;',
        #     'full': 'width: 100px;',
        # }
        # style = "width:%s;" % width_map.get(self.width, '300px')
        #style = "inline; width:100px;"
        style = ''
        if self.is_disabled():
            disabled_attr = "disabled"
        else:
            disabled_attr = ""

        if self.placeholder is not None:
            placeholder_attr = "placeholder='%s'" % self.placeholder
        else:
            placeholder_attr = ""

        is_invalid_class = self.get_is_invalid_class()
        #print("INFO: is_invalid_class = ", is_invalid_class)
        field_css_id = "%s_%s" % (self.form_css_id, self.name)
        input_html = f"<input type='{self.field_type}' id='{field_css_id}' class='form-control {is_invalid_class}' name='{self.name}' value='{value}' {placeholder_attr} style='{style}' {disabled_attr}>"
        # input_html = f"<input type='{self.field_type}' id='{field_css_id}' class='form-control' name='{self.name} {is_invalid_class}' value='{value}' {placeholder_attr} style='{style}' {disabled_attr}>" % (
        #     self.field_type, field_css_id, self.name, is_invalid_class, value, placeholder_attr, style, disabled_attr
        # )
        
        return self._field_tmpl(input_html), ""

class FormPasswordField(FormTextField):

    # field type can also be password
    def __init__(self, name, label=None, help=None, width=None, required=False, disabled=False, placeholder=None):
        super().__init__(name, label, help, required=required, disabled=disabled, field_type='password')

class FormEmailField(FormTextField):

    def __init__(self, name, label=None, help=None, width=None, required=False, disabled=False, placeholder=None):
        super().__init__(name, label, help, required=required, disabled=disabled, field_type='text')


    def _validate(self):
       
        try:

            email = self.value
            print("Email '%s'" % email)
            # Check that the email address is valid. Turn on check_deliverability
            # for first-time validations like on account creation pages (but not
            # login pages).
            emailinfo = validate_email(email, check_deliverability=False)

            # After this point, use only the normalized form of the email address,
            # especially before going to a database query.
            email = emailinfo.normalized

            return True, None

        except EmailNotValidError as e:

            # The exception message is human-readable explanation of why it's
            # not a valid (or deliverable) email address.
            print(str(e))

            return False, "Invalid email address"

    def validate_field(self, request):
        self.valid = super().validate_field(request)
        if not self.valid:
            return self.valid
        self.valid, self.error_msg = self._validate()
        return self.valid


class FormCaptchaField(FormInputField):

    def __init__(self, name, captcha_image_src,label=None, help=None, width=None, 
    required=False, disabled=False, placeholder=None):

        super().__init__(name, label, help, 
        required=required, disabled=disabled)
        self.captcha_image_src = captcha_image_src
        self.field_type = 'text'
    
    def get_captcha_choices(self, request):
        ip_addr = request.remote_addr
        ip_addr = ip_addr.replace(".", "")
        str_2_hash = "prefix_" + ip_addr
        result = hashlib.md5(str_2_hash.encode()).hexdigest().upper()
        return result

    def is_valid_captcha(self, request, code):
        if code is None:
            return False
        if len(code) != 4:
            return False
        choices = self.get_captcha_choices(request)
        # print("Choices:", choices)
        return code in choices

    def validate_field(self, request):
        self.valid = super().validate_field(request)
        if not self.valid:
            return self.valid
        code = self.value
        valid_captcha = self.is_valid_captcha(request, code)
        if not valid_captcha:
            self.valid, self.error_msg = (False, "Invalid captcha code")
            return self.valid
        self.valid, self.error_msg = (True, None)
        return self.valid

    def render(self):
        if self.value is None:
            value = ""
        else:
            value = self.value

        disabled_attr = ""
        placeholder_attr = ""

        style = ''
        is_invalid_class = self.get_is_invalid_class()
        field_css_id = "%s_%s" % (self.form_css_id, self.name)
        input_html = f"""
            <img src='{self.captcha_image_src}' alt='captcha' style='height: 100px;' />
            <input type='{self.field_type}' id='{field_css_id}' class='form-control {is_invalid_class}' name='{self.name}' value='{value}' {placeholder_attr} style='{style}' {disabled_attr}>
        """
        return self._field_tmpl(input_html), ""


# class FormCaptchaField(FormTextField):

#     def __init__(self, name, label=None, help=None, width=None, required=False, disabled=False, placeholder=None):
#         super().__init__(name, label, help, required=required, disabled=disabled, field_type='text')

#     def get_captcha_choices(request):
#         ip_addr = request.remote_addr
#         ip_addr = ip_addr.replace(".", "")
#         str_2_hash = "prefix_" + ip_addr
#         result = hashlib.md5(str_2_hash.encode()).hexdigest().upper()
#         return result

#     def is_valid_captcha(self, request, code):
#         if code is None:
#             return False
#         if len(code) != 4:
#             return False
#         choices = get_captcha_choices(request)
#         # print("Choices:", choices)
#         return code in choices


#     def _validate(self):
#         code = self.value
#         return (True, None)




# class FormNumberField(FormInputField):


#     def __init__(self, name, label=None, help=None, width=None, required=False, min=None, max=None):
#         super().__init__(name, label, help, required=required)
#         self.width = width
#         self.min = min
#         self.max = max

#     def min_value(self):
#         return self.min
    
#     def max_value(self):
#         return self.max
    

#     def render(self):
#         if self.value is None:
#             value = ""
#         else:
#             value = self.value

#         width_map = {
#             'small': 'width: 100px;',
#             'medium': 'width: 100px;',
#             'large': 'width: 100px;',
#             'full': 'width: 100px;',
#         }
#         style = "width:%s;" % width_map.get(self.width, '300px')
#         #style = "inline; width:100px;"

#         field_css_id = "%s_%s" % (self.form_css_id, self.name)
#         input_html = "<input type='text' id='%s' class='form-control' name='%s' value='%s' style='%s'>" % (field_css_id, self.name, value, style)
        
#         return self.wrap_label(input_html)

    

class FormHiddenField(FormInputField):

    def __init__(self, name, value=None):
        super().__init__(name)
        if value is not None:
            self._set_value(value)

    def _validate(self):
        return (True, None)

    def validate_field(self, request):
        return True

    def render(self):
        #id = "%s_%s" % (self.form_css_id, self.name)
        html = f"<input type='hidden' id='{self.name}' name='{self.name}' value='{self.value}'>"
        return html, ""


class FormTextAreaField(FormInputField):
    def __init__(self, name, label=None, help=None, required=False):
        super().__init__(name, label, help, required=required)

    def _validate(self):
        if self.required:
            if self.value is None or self.value == "":
                return (False, "Field is required")
        return (True, None)

    def validate_field(self, request):
        self.valid = super().validate_field(request)
        return self.valid


    def render(self):
        if self.value is None:
            value = ""
        else:
            value = self.value

        if self.is_disabled():
            disabled_attr = "disabled"
        else:
            disabled_attr = ""

        html = []
        #if self.label is not None:
        #    html.append("<label class='form-label'>%s</label>" % self.label)

        is_invalid_class = self.get_is_invalid_class()
        html.append(f"<textarea class='form-control {is_invalid_class}' id='{self.name}' name='{self.name}' rows='3' {disabled_attr}>{value}</textarea>")
        html = self._field_tmpl('\n'.join(html))
        return html, ""

class FormSelectField(FormInputField):

    def __init__(self, name, choices, label=None, help=None, required=False):
        super().__init__(name, label, help, required=required)
        self.choices = choices
        self.default = ''
        self.choices_map = {}
        for value, label, redirect_url in self.choices:
            self.choices_map[value] = label


    def _validate(self):
        selected = self.value
        if selected is None:
            return (True, "")
        if selected in self.choices_map:
            return (True, "")
        else:
            msg = "Value '%s' is not a valid value" % selected
            return (False, msg)


    def validate_field(self, request):
        self.valid = super().validate_field(request)
        if not self.valid:
            return self.valid
        self.valid, self.error_msg = self._validate()
        return self.valid

    # def render(self):
    #     selected = self.value
    #     css_id = "%s_%s" % (self.form_css_id, self.name)
    #     label = ""
    #     style = "width:45%;"
    #     f = "<select name='%s' id='%s' class='form-control form-select' aria-label='%s' style='%s'>" % (
    #         self.name,
    #         css_id,
    #         label,
    #         style,
    #     )
    #     for value, label, redirect_url in self.choices:
    #         selected_attr = ""
    #         selected_attr = ""
    #         if selected is not None:
    #             if selected == value:
    #                 selected_attr = "selected"
    #         else:
    #             if self.default == value:
    #                 selected_attr = "selected"

    #         f += "<option %s value='%s'>%s</option>" % (selected_attr, value, label)
    #     f += "</select>"
    #     return self._field_tmpl(f), ""

    def render(self):
        selected = self.value
        css_id = "%s_%s" % (self.form_css_id, self.name)
        label = ""
        style = "width:45%;"
        f = "<select name='%s' id='%s' class='form-control form-select' aria-label='%s' style='%s'>" % (
            self.name,
            css_id,
            label,
            style,
        )
        
        redirect_options = {}
        for value, label, redirect_url in self.choices:
            #print("Select field value: ", value, " label: ", label, " redirect_url: ", redirect_url)
            selected_attr = ""
            if selected is not None and selected == value:
                selected_attr = "selected"
            elif selected is None and self.default == value:
                selected_attr = "selected"

            f += "<option %s value='%s'>%s</option>" % (selected_attr, value, label)
            
            if redirect_url:
                redirect_options[value] = redirect_url

        f += "</select>"

        # Create a script to be added to the page footer
        js = """
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            var selectElement = document.getElementById('%s');
            var redirectOptions = %s;
            
            selectElement.addEventListener('change', function() {
                var selectedValue = this.value;
                if (redirectOptions.hasOwnProperty(selectedValue)) {
                    window.location.href = redirectOptions[selectedValue];
                }
            });
        });
        </script>
        """ % (css_id, json.dumps(redirect_options))

        # Return the select element HTML and the script separately
        return self._field_tmpl(f), js
    
