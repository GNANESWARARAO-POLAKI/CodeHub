from django import forms
from .models import *

class AddQuestionsForm(forms.ModelForm):
    score = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter score'}))
    class Meta:
        model=Questions
        fields=['title','description','score','timelimit']
    
class TestcaseForm(forms.ModelForm):
    class Meta:
        model=Testcases
        fields=['input_data','expected_output','hidden']


# forms.py
from django.forms import modelformset_factory

# Create the formset for the Testcase model
TestcaseFormSet = modelformset_factory(Testcases, form=TestcaseForm, extra=0)  # "extra=1" will show one empty form initially
