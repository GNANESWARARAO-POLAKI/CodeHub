from django import forms
from .models import User,Contests
import jinja2
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control',
        }),
        required=False 
    )
    username=forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'Enter user name'})
    )
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science'),
        ('ECE', 'Electronics and Communication'),
        ('ME', 'Mechanical Engineering'),
        ('EEE', 'Electrical Engineering'),
    ]
    YEAR_CHOICE=[
        (1,'First Year'),
        (2,'Second Year'),
        (3,'Third Year'),
        (4,'Fourth Year'),
    ]
    year=forms.ChoiceField(choices=YEAR_CHOICE,widget=forms.Select(attrs={'class':'form-select'}))
    branch = forms.ChoiceField(
        choices=BRANCH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'jntuno', 'branch', 'college', 'image']

    def __init__(self, *args, **kwargs):
        self.editable = kwargs.pop('editable',True)
        super().__init__(*args, **kwargs)
        if not self.editable:
            for field in ['username']:
                self.fields[field].widget.attrs['readonly'] = True
                self.fields[field].required = False
            self.fields['password'].widget = forms.HiddenInput()
        else:
            self.fields['password'].required = True

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not self.instance.pk: 
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("A user with that username already exists.")
        else:
            existing_user = User.objects.filter(username=username).exclude(pk=self.instance.pk)
            if existing_user.exists():
                raise forms.ValidationError("A user with that username already exists.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user 

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
    # Start Date Field
    start_date = forms.DateTimeField(
        widget=forms.DateInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        }, format='%Y-%m-%dT%H:%M')
    )

    # End Date Field
    end_date = forms.DateTimeField(
        widget=forms.DateInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        }, format='%Y-%m-%dT%H:%M')
    )

    # Contest Type Choices
    CONTEST_TYPES = [
        (1, "Compticode"),
        (2, "Codelife"),
    ]

    contest_type = forms.ChoiceField(
        choices=CONTEST_TYPES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Contests
        fields = ['title', 'description', 'start_date', 'end_date', 'venue', 'contest_type', 'poster']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Format initial values for start_date and end_date if editing an existing contest
        if self.instance and self.instance.pk:
            self.fields['start_date'].initial = self.instance.start_date.strftime('%Y-%m-%dT%H:%M')
            self.fields['end_date'].initial = self.instance.end_date.strftime('%Y-%m-%dT%H:%M')