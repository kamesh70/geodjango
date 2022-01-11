from django import forms
from django.forms import fields

from measurements.models import Measurement

class MeasurementModelForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields=('destination',)
