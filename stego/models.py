# encoding: utf-8
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with libstego.  If not, see <http://www.gnu.org/licenses/>.
#
#       Copyright 2009 2010 by Marko Krause <zeratul2099@googlemail.com>

from django.db import models
from django import forms

class CPTEmbedForm(forms.Form):
    message = forms.CharField(label='Nachricht', required=True)
    file = forms.FileField(required=True, label='PNG-Datei')
    pw = forms.CharField(label='Passwort',widget=forms.PasswordInput(render_value=False))
    matrix_values = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),) 
    height = forms.ChoiceField(choices=matrix_values, label='Blockhöhe')
    width = forms.ChoiceField(choices=matrix_values, label='Blockbreite')

class CPTExtractForm(forms.Form):
    file = forms.FileField(required=True, label='PNG-Datei')
    pw = forms.CharField(label='Passwort',widget=forms.PasswordInput(render_value=False))
    matrix_values = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),) 
    height = forms.ChoiceField(choices=matrix_values, label='Blockhöhe')
    width = forms.ChoiceField(choices=matrix_values, label='Blockbreite')

class F5EmbedForm(forms.Form):
    message = forms.CharField(label='Nachricht', required=True)
    file = forms.FileField(required=True, label='JPEG-Datei')
    pw = forms.CharField(label='Passwort',widget=forms.PasswordInput(render_value=False))

class F5ExtractForm(forms.Form):
    file = forms.FileField(required=True, label='JPEG-Datei')
    pw = forms.CharField(label='Passwort',widget=forms.PasswordInput(render_value=False))

class LsbEmbedForm(forms.Form):
    message = forms.CharField(label='Nachricht', required=True)
    file = forms.FileField(required=True, label='PNG-Datei')
    pw = forms.CharField(label='Passwort',widget=forms.PasswordInput(render_value=False))

class LsbExtractForm(forms.Form):
    file = forms.FileField(required=True, label='PNG-Datei')
    pw = forms.CharField(label='Passwort',widget=forms.PasswordInput(render_value=False))

class GifShuffleEmbedForm(forms.Form):
    message = forms.CharField(label='Nachricht', required=True)
    file = forms.FileField(required=True, label='GIF-Datei')
    pw = forms.CharField(label='Passwort',widget=forms.PasswordInput(render_value=False), required='False')

class GifShuffleExtractForm(forms.Form):
    file = forms.FileField(required=True, label='GIF-Datei')
    pw = forms.CharField(label='Passwort',widget=forms.PasswordInput(render_value=False), required='False')

class BattlestegEmbedForm(forms.Form):
    message = forms.CharField(label='Nachricht', required=True)
    file = forms.FileField(required=True, label='PNG-Datei')
    pw = forms.CharField(label='Passwort',widget=forms.PasswordInput(render_value=False))
    startbit_val = ((6,'2'),(7,'1'))
    move_away_val = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),)
    range_val = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),)
    startbit = forms.ChoiceField(choices=startbit_val, label='Farbbits')
    move_away = forms.ChoiceField(choices=move_away_val, label='Ranged Shots')
    range = forms.ChoiceField(choices=range_val, label='Range')

class BattlestegExtractForm(forms.Form):
    file = forms.FileField(required=True, label='PNG-Datei')
    pw = forms.CharField(label='Passwort',widget=forms.PasswordInput(render_value=False))
    startbit_val = ((6,'2'),(7,'1'))
    move_away_val = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),)
    range_val = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),)
    startbit = forms.ChoiceField(choices=startbit_val, label='Farbbits')
    move_away = forms.ChoiceField(choices=move_away_val, label='Ranged Shots')
    range = forms.ChoiceField(choices=range_val, label='Range')
