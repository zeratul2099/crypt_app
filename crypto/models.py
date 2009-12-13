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

class SimplestForm(forms.Form):
    message = forms.CharField(label='Klar-/Geheimtext', required=True)

class CaesarEncryptForm(forms.Form):
    message = forms.CharField(label='Klartext', required=True)
    key_values = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),
                    (7,'7'),(8,'8'),(9,'9'),(10,'10'),(11,'11'),(12,'12'),
                    (13,'13'),(14,'14'),(15,'15'),(16,'16'),(17,'17'),(18,'18'),
                    (19,'19'),(20,'20'),(21,'21'),(22,'22'),(23,'23'),(24,'24'),(25,'25')) 
    key = forms.ChoiceField(choices=key_values, label='Schluessel')

class CaesarDecryptForm(forms.Form):
    cypher_text = forms.CharField(label='Geheimtext', required=True)
    key_values = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),
                    (7,'7'),(8,'8'),(9,'9'),(10,'10'),(11,'11'),(12,'12'),
                    (13,'13'),(14,'14'),(15,'15'),(16,'16'),(17,'17'),(18,'18'),
                    (19,'19'),(20,'20'),(21,'21'),(22,'22'),(23,'23'),(24,'24'),(25,'25')) 
    key = forms.ChoiceField(choices=key_values, label='Schluessel')
    
class AffineEncryptForm(forms.Form):
    message = forms.CharField(label='Klartext', required=True)
    a_values = ((1,'1'),(3,'3'),(5,'5'),(7,'7'),(9,'9'),(11,'11'),(15,'15'),
                    (17,'17'),(19,'19'),(21,'21'),(23,'23'),(25,'25'))
    b_values = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),
                    (7,'7'),(8,'8'),(9,'9'),(10,'10'),(11,'11'),(12,'12'),
                    (13,'13'),(14,'14'),(15,'15'),(16,'16'),(17,'17'),(18,'18'),
                    (19,'19'),(20,'20'),(21,'21'),(22,'22'),(23,'23'),(24,'24'),(25,'25'))
    keyA = forms.ChoiceField(choices=a_values, label='Schluessel A')
    keyB = forms.ChoiceField(choices=b_values, label='Schluessel B')

class AffineDecryptForm(forms.Form):
    cypher_text = forms.CharField(label='Geheimtext', required=True)
    a_values = ((1,'1'),(9,'3'),(21,'5'),(15,'7'),(3,'9'),(19,'11'),(7,'15'),
                    (23,'17'),(11,'19'),(5,'21'),(17,'23'),(25,'25'))
    b_values = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),
                    (7,'7'),(8,'8'),(9,'9'),(10,'10'),(11,'11'),(12,'12'),
                    (13,'13'),(14,'14'),(15,'15'),(16,'16'),(17,'17'),(18,'18'),
                    (19,'19'),(20,'20'),(21,'21'),(22,'22'),(23,'23'),(24,'24'),(25,'25'))
    keyA = forms.ChoiceField(choices=a_values, label='Schluessel A')
    keyB = forms.ChoiceField(choices=b_values, label='Schluessel B')
