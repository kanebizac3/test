from django import forms
from .models import Post
from .models import Comments

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('text',)