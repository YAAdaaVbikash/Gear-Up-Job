from django import forms
from django.contrib.auth.models import User
from accounts.models import Company, Seeker
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SeekerSignUpForm(UserCreationForm):

    class Meta():
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class SeekerForm(forms.ModelForm):
    class Meta():
        model=Seeker
        fields=['job_category','full_name','job_category_1','job_category_2','job_category_3','job_category_4']


class CompanySignUpForm(UserCreationForm):

    class Meta():
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CompanyForm(forms.ModelForm):
    class Meta():
        model = Company
        fields = ['company_name', 'address', 'description',
                  'url', 'phone_number', 'profile_pic']

        widgets = {
            'description': forms.Textarea(attrs={'class': 'editable medium-editor-textarea my-textarea',
                                                 'style': 'width:400px;'}),
        }


class UserloginForm(AuthenticationForm):

    class Meta():
        model = User
        fields = ['username', 'password']
