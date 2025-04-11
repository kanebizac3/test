from django import forms
from .models import Post, Comments, GasolineOwada, PoiSute

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'image',) 
        # fields = ('title', 'text', )

class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('text', 'image',)

class GasolineOwadaForm(forms.ModelForm):

    class Meta:
        model = GasolineOwada
        fields = ('regular', 'deisel', )

class PoiSuteForm(forms.ModelForm):

    class Meta:
        model = PoiSute
        fields = ('latitude', 'longitude', 'image', 'description','reported_at')
        widgets = {
            'latitude': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'longitude': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
