from django import forms
from gearupjob.models import Job


class CreteJobForm(forms.ModelForm):
    class Meta():
        model = Job
        fields = ['title', 'job_type','job_category', 'job_location', 'application_deadline', 'salary',
                  'image', 'gender', 'vacancy', 'experience', 'responsibilities', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'application_deadline': forms.TextInput(attrs={'type': 'date'}),
            'responsibilities': forms.Textarea(attrs={'class': 'editable medium-editor-textarea my-textarea ',
                                                      }),
            'description': forms.Textarea(attrs={'class': 'editable medium-editor-textarea my-textarea',
                                                 }),
        }
