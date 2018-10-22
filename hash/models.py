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


from django import forms

class HashForm(forms.Form):
    clear = forms.CharField(label='Eingabe', required=False)
    fileH = forms.FileField(required=False, label='Datei')
    withSalt = forms.BooleanField(label='Mit Salz', required=False)

class Sha23Form(forms.Form):
    clear = forms.CharField(label='Eingabe', required=False)
    fileH = forms.FileField(required=False, label='Datei')
    withSalt = forms.BooleanField(label='Mit Salz', required=False)
    lenvals = ((1, '224'), (2, '256'), (3, '384'), (4, '512'),)
    hashlen = forms.ChoiceField(choices=lenvals, label='Hashlänge')
