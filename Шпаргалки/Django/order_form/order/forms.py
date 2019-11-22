from django import forms

from django.core.exceptions import ValidationError
import datetime


class SearchForm(forms.Form):
    query = forms.CharField(label='')
