from django import forms
from .models import Map, Gomimon

class MapForm(forms.ModelForm):

    class Meta:
        model = Map
        fields = ('latitude', 'longitude', 'image', 'description','reported_at',"category", "picking")
        widgets = {
            'latitude': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'longitude': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

# ------ユーザー登録---------
from django.contrib.auth.models import User

class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='ユーザー名', max_length=150, help_text='必須。150文字以内。文字、数字、@/./+/-/_が使えます。')
    email = forms.EmailField(label='メールアドレス', required=False)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    password2 = forms.CharField(label='パスワード (確認)', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("このユーザー名は既に使用されています。")
        return username

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data['password2']
        if password is not None and password != password2:
            raise forms.ValidationError("パスワードが一致しません。")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'], self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    


from .models import Gomimon, GomimonType

class CreateGomimonForm(forms.ModelForm):
    gomimon_type = forms.ChoiceField(choices=GomimonType.choices)

    class Meta:
        model = Gomimon
        fields = ('name', 'image', 'gomimon_type', 'hp', 'attack', 'defense', 'skill', 'skill_effect')