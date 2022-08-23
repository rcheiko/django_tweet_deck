from django import forms
from .models import *

class GivePerm(forms.Form):
    user = forms.CharField(required=True)