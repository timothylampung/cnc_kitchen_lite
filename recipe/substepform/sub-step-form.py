from crispy_forms.layout import Layout, Column, Row, Div, Submit, Button, Hidden
from django.forms import ModelForm, Form
from crispy_forms.helper import FormHelper


class HeaterForm(Form):
    


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
        super(HeaterForm, self).__init__(*args, **kwargs)
