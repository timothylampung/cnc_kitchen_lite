from crispy_forms.layout import Layout, Column, Row, Div, Submit, Button, Hidden
from django import forms
from django.forms import ModelForm, Form
from crispy_forms.helper import FormHelper
from recipe.models import Recipe, Step
from tasks.models import TaskSet


class TaskSetForm(ModelForm):
    class Meta:
        model = TaskSet
        exclude = ['document_status', 'document_code', 'creator', 'editor', ]

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '/tasks/add-step/'
        self.helper.form_class = 'add-to-task-form'
        self.helper.layout = Layout(
            Div(
                Div('recipe', css_class='form-group col-md-12'),
                Div('task_name', css_class='form-group col-md-12'),
                css_class='modal-body'
            ),
            Div(
                Button('button', 'Cancel', css_class='btn btn-secondary'),
                Submit('submit', 'Add Steps', id='wtf-btn', css_class='btn btn-primary'),
                css_class='modal-footer'
            ),
        )
        super(TaskSetForm, self).__init__(*args, **kwargs)
