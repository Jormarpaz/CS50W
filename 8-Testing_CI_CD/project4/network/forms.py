from django import forms

class NewPostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'What\'s on your mind?',
        'rows': 3,
        'cols': 50
    }), label="")