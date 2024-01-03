from django import forms
from blog.models import Post, Yorum

class YeniPostForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)
    title = forms.CharField(max_length=200)

    class Meta:
        model = Post
        fields = ['image', 'text', 'created_date', 'title']

class YorumForm(forms.ModelForm):
    class Meta:
        model = Yorum
        fields = ['isim', 'yorum']

        widgets = {
            'İsim': forms.TextInput(attrs={'class': 'form-control'}),
            'Yorum': forms.Textarea(attrs={'class': 'form-control'}),
        }
