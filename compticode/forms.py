from django import forms
from .models import *
from django.core import serializers

class AddQuestionsForm(forms.ModelForm):
    score = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter score'}))
    class Meta:
        model=Question
        fields=['title','description','score','timelimit']
    
class TestcaseForm(forms.ModelForm):
    class Meta:
        model=Testcase
        fields=['input_data','expected_output','hidden']


# forms.py
from django.forms import modelformset_factory

# Create the formset for the Testcase model with the ability to add and delete test cases
TestcaseFormSet = modelformset_factory(Testcase, form=TestcaseForm, can_delete=True)
 
