from django.db import models
from django import forms

class HashForm(forms.Form):
    clear = forms.CharField(label='Input String')
    file = forms.FileField(required=False)
    hashes = (('md5', 'MD5'), ('sha1', 'SHA-1'),
              ('sha224', 'SHA-224'), ('sha256', 'SHA-256'),
              ('sha384', 'SHA-384'), ('sha512', 'SHA-512'),
             )
    algorithm = forms.ChoiceField(choices=hashes, label='Algorithm')

