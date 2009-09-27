from django.db import models
from django import forms

class CPTEmbedForm(forms.Form):
    message = forms.CharField(label='Nachricht', required=True)
    file = forms.FileField(required=True, label='PNG-Datei')
    pw = forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))
    matrix_values = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),) 
    height = forms.ChoiceField(choices=matrix_values, label='Blockhoehe')
    width = forms.ChoiceField(choices=matrix_values, label='Blockbreite')

class CPTExtractForm(forms.Form):
    file = forms.FileField(required=True, label='PNG-Datei')
    pw = forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))
    matrix_values = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),) 
    height = forms.ChoiceField(choices=matrix_values, label='Blockhoehe')
    width = forms.ChoiceField(choices=matrix_values, label='Blockbreite')

class F5EmbedForm(forms.Form):
    message = forms.CharField(label='Nachricht', required=True)
    file = forms.FileField(required=True, label='JPEG-Datei')
    pw = forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))

class F5ExtractForm(forms.Form):
    file = forms.FileField(required=True, label='JPEG-Datei')
    pw = forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))
