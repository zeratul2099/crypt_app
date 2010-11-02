# -*- coding: utf-8 -*-
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

from crypt_app.hash.models import HashForm, Sha2Form, KeccakForm
from crypt_app.base_app.models import Algo, InfoPage, ManPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader
from KeccakHash import KeccakHash
from datetime import datetime
import hashlib, random, sys
import keccak.Keccak

def algo(request, algo):
    salt = 0
    salt_str = ''
    algo_object = get_object_or_404(Algo, shortTitle=algo)
    manual = get_object_or_404(ManPage, algo=algo_object)
    hash_val = ""
    if request.method == 'POST':
        
        if request.FILES:
            #if request.FILES['fileH'].size > 10000 and algo=="keccak":
            #    form = HashForm()
            #    return render_to_response("hash_algo.html", {'hashvalue' : 'Datei zu gross',  'form' : form}) 
            clear_text = request.FILES['fileH'].read()
            output = "Eingabedatei:\n%s (%s Bytes)\n" %(request.FILES['fileH'].name,
                                                      request.FILES['fileH'].size)
        else:
            clear_text = request.POST.get("clear", "")
            output = "Eingabestring:\n%s\n\n" %(clear_text)
            
        if 'withSalt' in request.POST:
            rand = random.Random(datetime.now().strftime('%s'))
            salt = rand.randint(0, sys.maxint)
            for i in range(4):
                salt_str += chr((salt%(1<<(8*(i+1))))>>((i*8)+1))
            clear_text += salt_str
            
        form = HashForm(request.POST, request.FILES)
        if algo == "keccak":
            form = KeccakForm(request.POST, request.FILES)
            params = {"1":(1152,448,28,224),
                      "2":(1088,512,32,256),
                      "3":(832,768,48,384),
                      "4":(576,1024,64,512),
                      }
            l = request.POST["hashlen"]
            output += "Keccak[1600]-"+str(params[l][3])+"-Hash:\n"
            #hash_val = KeccakHash(repr(clear_text)).hexdigest()
            myKeccak=keccak.Keccak.Keccak()
            inputHex = clear_text.encode("hex")

            hash_val = myKeccak.Keccak((4*len(inputHex),inputHex),params[l][0],params[l][1],params[l][2],params[l][3])
        elif algo == "md5":
            output += "MD5-Hash:\n"
            hash_val = hashlib.md5(clear_text).hexdigest()
        elif algo == "sha1":
            output += "SHA-1-Hash:\n"
            hash_val = hashlib.sha1(clear_text).hexdigest()
        elif algo == "sha2":
            form = Sha2Form(request.POST, request.FILES)
            hashlen = request.POST['hashlen']
            if hashlen == '1':
                output += "SHA-2-224-Hash:\n"
                hash_val = hashlib.sha224(clear_text).hexdigest()
            elif hashlen == '2':
                output += "SHA-2-256-Hash:\n"
                hash_val = hashlib.sha256(clear_text).hexdigest()
            elif hashlen == '3':
                output += "SHA-2-384-Hash:\n"
                hash_val = hashlib.sha384(clear_text).hexdigest()
            elif hashlen == '4':
                output += "SHA-2-512-Hash:\n"
                hash_val = hashlib.sha512(clear_text).hexdigest()   
        else:
            output += u"Ungültiger Algorithmus"
        if 'withSalt' in request.POST:
            output += "\n\nSalz:\n"
            output += repr(salt_str)
    else:
        clear_text = ""
        output = ''
        if algo == 'sha2':
            form = Sha2Form()
        elif algo == 'keccak':
            form = KeccakForm()
        else:
            form = HashForm()
    return render_to_response("hash_algo.html", {'algo' : algo_object,
                                            'hashvalue' : output,
                                            'hash' : hash_val,
                                            'clear_text' : clear_text,
                                            'form' : form,
                                            'algo_type' : 'Hash-Algorihmen',
                                            'manual' : manual,}) 
