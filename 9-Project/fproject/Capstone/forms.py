from django import forms
from .models import File, Folder, Event

class UploadFile(forms.ModelForm):
    class Meta:
        model = File
        fields = ["name", "file", "folder", "tags"]

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ["name", "parent"]

class CreateSubfolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

class UploadFileInFolderForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start', 'end', 'allDay']
        widgets = {
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
        
    def clean(self):
        cleaned_data = super().clean()
        allDay = cleaned_data.get("allDay")
        end = cleaned_data.get("end")

        # Si es "todo el día", no es necesario el campo "end"
        if allDay and end:
            cleaned_data["end"] = None

        return cleaned_data