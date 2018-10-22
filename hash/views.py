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

from datetime import datetime
import hashlib
import random
import sys

from django.shortcuts import get_object_or_404, render_to_response

from models import HashForm, Sha23Form
from ..base_app.models import Algo, ManPage

# pylint: disable=too-many-locals,too-many-branches
def algo(request, algo_name):
    salt = 0
    salt_str = ''
    algo_object = get_object_or_404(Algo, shortTitle=algo_name)
    manual = get_object_or_404(ManPage, algo=algo_object)
    hash_val = ""
    if request.method == 'POST':

        if request.FILES:
            clear_text = request.FILES['fileH'].read()
            output = "Eingabedatei:\n%s (%s Bytes)\n" % (
                request.FILES['fileH'].name,
                request.FILES['fileH'].size
            )
        else:
            clear_text = request.POST.get("clear", "")
            output = "Eingabestring:\n%s\n\n" %(clear_text)

        if 'withSalt' in request.POST:
            rand = random.Random(datetime.now().strftime('%s'))
            salt = rand.randint(0, sys.maxsize)
            for i in range(4):
                salt_str += chr((salt%(1<<(8*(i+1))))>>((i*8)+1))
            clear_text += salt_str

        form = HashForm(request.POST, request.FILES)
        if algo_name == "md5":
            output += "MD5-Hash:\n"
            hash_val = hashlib.md5(clear_text.encode('utf8')).hexdigest()
        elif algo_name == "sha1":
            output += "SHA-1-Hash:\n"
            hash_val = hashlib.sha1(clear_text.encode('utf8')).hexdigest()
        elif algo_name in ["sha2", "keccak"]:
            hashlen = request.POST['hashlen']
            lengths = [224, 256, 384, 512]
            form = Sha23Form(request.POST, request.FILES)
            if algo_name == "sha2":
                ver = "2"
                hash_f = {
                    "1": hashlib.sha224,
                    "2": hashlib.sha256,
                    "3": hashlib.sha384,
                    "4": hashlib.sha512,
                }
            else:
                ver = "3"
                hash_f = {
                    "1": hashlib.sha3_224,
                    "2": hashlib.sha3_256,
                    "3": hashlib.sha3_384,
                    "4": hashlib.sha3_512,
                }

            output += "SHA-%s-%s-Hash:\n" % (ver, lengths[hashlen])
            hash_val = hash_f[hashlen](clear_text.encode('utf8')).hexdigest()
        else:
            output += "Ungültiger Algorithmus"
        if 'withSalt' in request.POST:
            output += "\n\nSalz:\n"
            output += repr(salt_str)
    else:
        clear_text = ""
        output = ''
        if algo_name in ['sha2', 'keccak']:
            form = Sha23Form()
        else:
            form = HashForm()
    return render_to_response("hash_algo.html", {
        'algo': algo_object,
        'hashvalue': output,
        'hash': hash_val,
        'clear_text': clear_text,
        'form': form,
        'algo_type': 'Hash-Algorihmen',
        'manual': manual,
    })
# pylint: enable=too-many-locals,too-many-branches
