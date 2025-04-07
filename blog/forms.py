from django import forms
from .models import Post
from .models import Comments
from .models import GasolineOwada

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        # fields = ('title', 'text', 'image',) 
        fields = ('title', 'text', )

class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('text',)

class GasolineOwadaForm(forms.ModelForm):

    class Meta:
        model = GasolineOwada
        fields = ('regular', 'deisel', )
