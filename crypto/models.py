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

class AESEncryptForm(forms.Form):
    message = forms.CharField(label='Klartext', required=True)
    key = forms.IntegerField(label=u'Schlüssel (große Zahl)', required=True)
    block_values = ((1,'ECB'),(2,'CBC'),(3,'CFB')) 
    block_mode = forms.ChoiceField(choices=block_values, label='Blockmodus')

class AESDecryptForm(forms.Form):
    cypher_text = forms.IntegerField(label='Geheimtext', required=True)
    key = forms.IntegerField(label=u'Schlüssel (große Zahl)', required=True)
    block_values = ((1,'ECB'),(2,'CBC'),(3,'CFB')) 
    block_mode = forms.ChoiceField(choices=block_values, label='Blockmodus')


class SimpleEncryptForm(forms.Form):
    message = forms.CharField(label='Klartext', required=True)
    key = forms.IntegerField(label=u'Schlüssel (große Zahl)', required=True)

class SimpleDecryptForm(forms.Form):
    cypher_text = forms.IntegerField(label='Geheimtext', required=True)
    key = forms.IntegerField(label=u'Schlüssel (große Zahl)', required=True)

class RSAEncryptForm(forms.Form):
    message = forms.CharField(label='Klartext', required=True)
    key = forms.FileField(label=u'Öffentlicher Schlüssel', required=True)

class RSADecryptForm(forms.Form):
    cypher_text = forms.IntegerField(label='Geheimtext', required=True)
    key = forms.FileField(label=u'Privater Schluessel', required=True)

class SimplestForm(forms.Form):
    message = forms.CharField(label=u'Klar-/Geheimtext', required=True)

class CaesarEncryptForm(forms.Form):
    message = forms.CharField(label=u'Klartext', required=True)
    key_values = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),
                    (7,'7'),(8,'8'),(9,'9'),(10,'10'),(11,'11'),(12,'12'),
                    (13,'13'),(14,'14'),(15,'15'),(16,'16'),(17,'17'),(18,'18'),
                    (19,'19'),(20,'20'),(21,'21'),(22,'22'),(23,'23'),(24,'24'),(25,'25')) 
    key = forms.ChoiceField(choices=key_values, label=u'Schlüssel')

class CaesarDecryptForm(forms.Form):
    cypher_text = forms.CharField(label='Geheimtext', required=True)
    key_values = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),
                    (7,'7'),(8,'8'),(9,'9'),(10,'10'),(11,'11'),(12,'12'),
                    (13,'13'),(14,'14'),(15,'15'),(16,'16'),(17,'17'),(18,'18'),
                    (19,'19'),(20,'20'),(21,'21'),(22,'22'),(23,'23'),(24,'24'),(25,'25')) 
    key = forms.ChoiceField(choices=key_values, label=u'Schlüssel')
    
class AffineEncryptForm(forms.Form):
    message = forms.CharField(label='Klartext', required=True)
    a_values = ((1,'1'),(3,'3'),(5,'5'),(7,'7'),(9,'9'),(11,'11'),(15,'15'),
                    (17,'17'),(19,'19'),(21,'21'),(23,'23'),(25,'25'))
    b_values = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),
                    (7,'7'),(8,'8'),(9,'9'),(10,'10'),(11,'11'),(12,'12'),
                    (13,'13'),(14,'14'),(15,'15'),(16,'16'),(17,'17'),(18,'18'),
                    (19,'19'),(20,'20'),(21,'21'),(22,'22'),(23,'23'),(24,'24'),(25,'25'))
    keyA = forms.ChoiceField(choices=a_values, label=u'Schlüssel A')
    keyB = forms.ChoiceField(choices=b_values, label=u'Schlüssel B')

class AffineDecryptForm(forms.Form):
    cypher_text = forms.CharField(label='Geheimtext', required=True)
    a_values = ((1,'1'),(9,'3'),(21,'5'),(15,'7'),(3,'9'),(19,'11'),(7,'15'),
                    (23,'17'),(11,'19'),(5,'21'),(17,'23'),(25,'25'))
    b_values = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),
                    (7,'7'),(8,'8'),(9,'9'),(10,'10'),(11,'11'),(12,'12'),
                    (13,'13'),(14,'14'),(15,'15'),(16,'16'),(17,'17'),(18,'18'),
                    (19,'19'),(20,'20'),(21,'21'),(22,'22'),(23,'23'),(24,'24'),(25,'25'))
    keyA = forms.ChoiceField(choices=a_values, label=u'Schlüssel A')
    keyB = forms.ChoiceField(choices=b_values, label=u'Schlüssel B')
