from django.db import models
from django import forms

class AESEncryptForm(forms.Form):
    message = forms.CharField(label='Klartext', required=True)
    key = forms.IntegerField(label='Schluessel (grosse Zahl)', required=True)
    block_values = ((1,'ECB'),(2,'CBC'),(3,'CFB')) 
    block_mode = forms.ChoiceField(choices=block_values, label='Blockmodus')

class AESDecryptForm(forms.Form):
    cypher_text = forms.IntegerField(label='Geheimtext', required=True)
    key = forms.IntegerField(label='Schluessel (grosse Zahl)', required=True)
    block_values = ((1,'ECB'),(2,'CBC'),(3,'CFB')) 
    block_mode = forms.ChoiceField(choices=block_values, label='Blockmodus')


class SimpleEncryptForm(forms.Form):
    message = forms.CharField(label='Klartext', required=True)
    key = forms.IntegerField(label='Schluessel (grosse Zahl)', required=True)

class SimpleDecryptForm(forms.Form):
    cypher_text = forms.IntegerField(label='Geheimtext', required=True)
    key = forms.IntegerField(label='Schluessel (grosse Zahl)', required=True)

class RSAEncryptForm(forms.Form):
    message = forms.CharField(label='Klartext', required=True)
    key = forms.FileField(label='Public Key', required=True)

class RSADecryptForm(forms.Form):
    cypher_text = forms.IntegerField(label='Geheimtext', required=True)
    key = forms.FileField(label='Private Key', required=True)

