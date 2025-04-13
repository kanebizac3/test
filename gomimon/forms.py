from django import forms
from .models import Map



class MapForm(forms.ModelForm):

    class Meta:
        model = Map
        fields = ('latitude', 'longitude', 'image', 'description','reported_at')
        widgets = {
            'latitude': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'longitude': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
