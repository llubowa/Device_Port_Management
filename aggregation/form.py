from django import forms
from .models import aggregation_hubs

class HubForm(forms.ModelForm):
    class Meta:
        model = aggregation_hubs
        fields = "__all__"