from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django import forms


class HeaterForm(forms.Form):
    switch_heater_front = forms.BooleanField(
        label="",
        widget=forms.CheckboxInput,
        initial='0',
        required=False,
    )

    front_target_temperature = forms.IntegerField(
        label="Front Target Temperature",
        required=False,
    )

    switch_heater_back = forms.BooleanField(
        label="Back Heater",
        widget=forms.CheckboxInput,
        initial='0',
        required=False,
    )

    back_target_temperature = forms.IntegerField(
        label="Back Target Temperature",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('front_target_temperature', css_class="form-control"),
                    css_class='col-md-10'
                ),
                Div(
                    Field('switch_heater_front', css_class='form-check-input '),
                    css_class='form-check form-switch form-check-custom form-check-solid col-md-2'
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('back_target_temperature', css_class="form-control"),
                    css_class='col-md-10'
                ),
                Div(
                    Field('switch_heater_back', css_class='form-check-input '),
                    css_class='form-check form-switch form-check-custom form-check-solid col-md-2'
                ),
                css_class="row"
            )
        )


class MixerForm(forms.Form):
    MIXER_MODES = [
        ('MOVE', 'MOVE'),
        ('MIX', 'MIX'),
        ('DISPENSE', 'DISPENSE'),
        ('ZERO', 'ZERO')
    ]

    mixer_mode = forms.ChoiceField(choices=MIXER_MODES, widget=forms.Select(attrs={'class': "form-control"}))

    mixer_speed = forms.IntegerField(
        label="Mixer Speed",
        required=False,
    )


class ValveForm(forms.Form):
    open_water_valve = forms.TypedChoiceField(
        label="",
        widget=forms.CheckboxInput,
        initial='0',
        required=False,
    )

    open_water_valve_duration = forms.IntegerField(
        label="Open water valve duration",
        required=False,
    )

    open_oil_valve = forms.TypedChoiceField(
        label="",
        widget=forms.CheckboxInput,
        initial='0',
        required=False,
    )

    open_oil_valve_duration = forms.IntegerField(
        label="Open oil valve duration",
        required=False,
    )

    open_water_jet_valve = forms.TypedChoiceField(
        label="",
        widget=forms.CheckboxInput,
        initial='0',
        required=False,
    )

    open_water_jet_valve_duration = forms.IntegerField(
        label="Open water jet valve duration",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Div(
                Div(
                    Field('open_water_valve_duration', css_class="form-control"),
                    css_class='col-md-10'
                ),
                Div(
                    Field('open_water_valve', css_class='form-check-input '),
                    css_class='form-check form-switch form-check-custom form-check-solid col-md-2'
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('open_oil_valve_duration', css_class="form-control"),
                    css_class='col-md-10'
                ),
                Div(
                    Field('open_oil_valve', css_class='form-check-input '),
                    css_class='form-check form-switch form-check-custom form-check-solid col-md-2'
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('open_water_jet_valve_duration', css_class="form-control"),
                    css_class='col-md-10'
                ),
                Div(
                    Field('open_water_jet_valve', css_class='form-check-input '),
                    css_class='form-check form-switch form-check-custom form-check-solid col-md-2'
                ),
                css_class="row"
            ),
        )
