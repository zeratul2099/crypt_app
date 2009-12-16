# encoding: utf-8
from django.db import models
from django import forms

class HashForm(forms.Form):
    clear = forms.CharField(label='Eingabe', required=False)
    file = forms.FileField(required=False, label='Datei')
    withSalt = forms.BooleanField(label='Mit Salz', required=False)

class Sha2Form(forms.Form):
    clear = forms.CharField(label='Eingabe', required=False)
    file = forms.FileField(required=False, label='Datei')
    withSalt = forms.BooleanField(label='Mit Salz', required=False)
    lenvals = ((1,'224'),(2,'256'),(3,'384'),(4,'512'),) 
    hashlen = forms.ChoiceField(choices=lenvals, label='Hashlänge')

