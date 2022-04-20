from crispy_forms.layout import Layout, Column, Row, Div, Submit
from django import forms
from django.forms import ModelForm
from tinymce import TinyMCE
from crispy_forms.helper import FormHelper
from module.models import Module


class ModuleForm(ModelForm):
    class Meta:
        model = Module
        exclude = ['document_status', 'document_code', 'creator', 'editor']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '/modules/create/'
        self.helper.layout = Layout(
            Div(
                Div('name', css_class='form-group col-md-12'),
                css_class='row'
            ),
            Div(
                Div('type_handler', css_class='form-group col-md-4'),
                Div('ip_address', css_class='form-group col-md-4'),
                Div('port', css_class='form-group col-md-4'),
                css_class='row'
            ),
            Submit('submit', 'Create', css_class='mt-4 col-12')
        )

        super(ModuleForm, self).__init__(*args, **kwargs)
