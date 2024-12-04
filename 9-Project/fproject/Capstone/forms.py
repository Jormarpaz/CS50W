from django import forms
from .models import File

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name','file','description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del archivo'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del archivo'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nombre del archivo',
            'description': 'Descripción del archivo',
            'file': 'Seleccionar Archivo',
        }