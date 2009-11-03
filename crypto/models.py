from django.db import models
from django import forms

class AESEncryptForm(forms.Form):
    message = forms.CharField(label='Nachricht', required=True)
    key = forms.IntegerField(label='Schluessel (grosse Zahl)', required=True)
    block_values = ((1,'ECB'),(2,'CBC'),(3,'CFB')) 
    block_mode = forms.ChoiceField(choices=block_values, label='Blockmodus')

class AESDecryptForm(forms.Form):
    cypher_text = forms.IntegerField(label='Chiffre', required=True)
    key = forms.IntegerField(label='Schluessel (grosse Zahl)', required=True)
    block_values = ((1,'ECB'),(2,'CBC'),(3,'CFB')) 
    block_mode = forms.ChoiceField(choices=block_values, label='Blockmodus')

