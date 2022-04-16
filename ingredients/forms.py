from crispy_forms.layout import Layout, Column, Row, Div, Submit
from django import forms
from django.forms import ModelForm
from tinymce import TinyMCE
from crispy_forms.helper import FormHelper
from ingredients.models import Ingredient


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        exclude = ['document_status', 'document_code', 'creator', 'editor']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '/ingredients/create/'
        self.helper.layout = Layout(
            Div(
                Div('image_path', css_class='form-group col-md-12'),
                css_class='row'
            ),
            Div(
                Div('ingredient_name', css_class='form-group col-md-12'),
                css_class='row'
            ), Div(
                Div('stock_count', css_class='form-group col-md-6'),
                Div('invoked_count', css_class='form-group col-md-6'),
                css_class='row'
            ),
            Div(
                Div('type', css_class='form-group col-md-6'),
                Div('unit', css_class='form-group col-md-6'),
                css_class='row'
            ),

            Submit('submit', 'Create', css_class='mt-4 col-12')
        )

        super(IngredientForm, self).__init__(*args, **kwargs)
