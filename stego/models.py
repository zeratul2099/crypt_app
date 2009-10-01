from django.db import models
from django import forms

class CPTEmbedForm(forms.Form):
    message = forms.CharField(label='Nachricht', required=True)
    file = forms.FileField(required=True, label='PNG-Datei')
    pw = forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))
    matrix_values = ((1,'1'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8')) 
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

class LsbEmbedForm(forms.Form):
    message = forms.CharField(label='Nachricht', required=True)
    file = forms.FileField(required=True, label='PNG-Datei')
    pw = forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))

class LsbExtractForm(forms.Form):
    file = forms.FileField(required=True, label='PNG-Datei')
    pw = forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))

class GifShuffleEmbedForm(forms.Form):
    message = forms.CharField(label='Nachricht', required=True)
    file = forms.FileField(required=True, label='GIF-Datei')
    pw = forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))

class GifShuffleExtractForm(forms.Form):
    file = forms.FileField(required=True, label='GIF-Datei')
    pw = forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))

class BattlestegEmbedForm(forms.Form):
    message = forms.CharField(label='Nachricht', required=True)
    file = forms.FileField(required=True, label='PNG-Datei')
    pw = forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))
    startbit_val = ((6,'6'),(7,'7'))
    move_away_val = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),)
    range_val = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),)
    startbit = forms.ChoiceField(choices=startbit_val, label='Farbbits ignorieren')
    move_away = forms.ChoiceField(choices=move_away_val, label='Wieviel Ranged Shots')
    range = forms.ChoiceField(choices=range_val, label='Range')

class BattlestegExtractForm(forms.Form):
    file = forms.FileField(required=True, label='PNG-Datei')
    pw = forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))
    startbit_val = ((6,'6'),(7,'7'))
    move_away_val = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),)
    range_val = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),)
    startbit = forms.ChoiceField(choices=startbit_val, label='Farbbits ignorieren')
    move_away = forms.ChoiceField(choices=move_away_val, label='Wieviel Ranged Shots')
    range = forms.ChoiceField(choices=range_val, label='Range')
