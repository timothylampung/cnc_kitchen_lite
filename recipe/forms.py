from crispy_forms.layout import Layout, Column, Row, Div, Submit, Button, Hidden
from django import forms
from django.forms import ModelForm, Form
from crispy_forms.helper import FormHelper
from recipe.models import Recipe, Step


class RecipeForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Recipe
        exclude = ['document_status', 'document_code', 'creator', 'editor']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '/recipes/create/'
        self.helper.layout = Layout(
            Div(
                Div('image_path', css_class='form-group col-md-12'),
                css_class='row'
            ), Div(
                Div('recipe_name', css_class='form-group col-md-12'),
                css_class='row'
            ),
            Div(
                Div('recipe_author', css_class='form-group col-md-8'),
                Div('queue_handler', css_class='form-group col-md-4'),
                css_class='row'
            ), Div(
                Div('description', css_class='form-group col-md-12'),
                css_class='row'
            ),
            Submit('submit', 'Create', css_class='mt-4 col-12')
        )

        super(RecipeForm, self).__init__(*args, **kwargs)


class StepForm(ModelForm):
    class Meta:
        model = Step
        exclude = ['document_status', 'document_code', 'creator', 'editor', ]

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '/recipes/add-step/'
        self.helper.layout = Layout(
            Div(
                Div('step_name', css_class='form-group col-md-12'),
                Div('wait_for', css_class='form-group col-md-12'),
                Div('recipe', css_class='form-group col-md-12'),
                Div('step_type', css_class='form-group col-md-12'),
                css_class='modal-body'
            ),
            Div(
                Button('button', 'Cancel', css_class='btn btn-secondary'),
                Submit('submit', 'Add Steps', css_class='btn btn-primary'),
                css_class='modal-footer'
            ),
        )
        super(StepForm, self).__init__(*args, **kwargs)


class MainForm(Form):
    class Meta:
        pass

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '/recipes/add-step/'
        self.helper.layout = Layout(
            Div(
                Div('step_name', css_class='form-group col-md-12'),
                Div('wait_for', css_class='form-group col-md-12'),
                Div('recipe', css_class='form-group col-md-12'),
                Div('step_type', css_class='form-group col-md-12'),
                css_class='modal-body'
            ),
            Div(
                Button('button', 'Cancel', css_class='btn btn-secondary'),
                Submit('submit', 'Add Steps', css_class='btn btn-primary'),
                css_class='modal-footer'
            ),
        )
        super(MainForm, self).__init__(*args, **kwargs)
