from django import forms
from .models import *

class AddQuestionsForm(forms.ModelForm):
    score = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter score'}))
    class Meta:
        model=Questions
        fields=['title','descreption','score','timelimit']
    