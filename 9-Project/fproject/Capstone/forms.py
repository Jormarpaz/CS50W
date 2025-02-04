from django import forms
from .models import File, Folder

class UploadFile(forms.ModelForm):
    class Meta:
        model = File
        fields = ["name", "file", "folder", "tags"]

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["name", "file", "tags", "folder"]

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ["name"]