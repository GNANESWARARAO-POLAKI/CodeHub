from django import forms
from .models import User,Contests

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        'class': 'form-control',
    }))
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science'),
        ('ECE', 'Electronics and Communication'),
        ('ME', 'Mechanical Engineering'),
        ('EEE', 'Electrical Engineering'),
    ]
    branch = forms.ChoiceField(choices=BRANCH_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select',
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'jntuno', 'branch', 'college', 'image']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'Enter your username',
        'class': 'form-control',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        'class': 'form-control',
    }))

class ContestCreationForm(forms.ModelForm):
    contest_type=forms.ChoiceField(choices=[(1,'CodeLife'),(2,'ComptiCode'),(3,'DebugCode')],widget=forms.Select(attrs={'class':'from-select',}))
    start_date=forms.DateTimeField(widget=forms.DateInput(attrs={
        'type': 'datetime-local',
        'class': 'form-control',
    }, format='%Y-%m-%dT%H:%M'))
    end_date=forms.DateTimeField(widget=forms.DateInput(attrs={
        'type': 'datetime-local',
        'class': 'form-control',
    }, format='%Y-%m-%dT%H:%M'))
    class Meta:
        model=Contests
        fields=['title','description','start_date','end_date','venue','contest_type','poster','contest_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Format the initial data for start_date and end_date
            self.fields['start_date'].initial = self.instance.start_date.strftime('%Y-%m-%dT%H:%M')
            self.fields['end_date'].initial = self.instance.end_date.strftime('%Y-%m-%dT%H:%M')
    