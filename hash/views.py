# encoding: utf-8
from crypt_app.hash.models import HashForm, Sha2Form
from crypt_app.base_app.models import Algo, InfoPage, ManPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader
from KeccakHash import KeccakHash
from datetime import datetime
import hashlib, random, sys


def algo(request, algo):
    salt = 0
    salt_str = ''
    algo_object = get_object_or_404(Algo, shortTitle=algo)
    manual = get_object_or_404(ManPage, algo=algo_object)
    hash_val = ""
    if request.method == 'POST':
        
        if request.FILES:
            if request.FILES['file'].size > 10000 and algo=="keccak":
                form = HashForm()
                return render_to_response("hash_algo.html", {'hashvalue' : 'Datei zu gross',  'form' : form}) 
            clear_text = request.FILES['file'].read()
            output = "Eingabedatei:\n%s (%s Bytes)\n" %(request.FILES['file'].name,
                                                      request.FILES['file'].size)
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
            output += "Keccak[800]-224-Hash:\n"
            hash_val = KeccakHash(repr(clear_text)).hexdigest()
        elif algo == "md5":
            output += "MD5-Hash:\n"
            hash_val = hashlib.md5(clear_text).hexdigest()
            #output += hash_val 
        elif algo == "sha1":
            output += "SHA-1-Hash:\n"
            hash_val = hashlib.sha1(clear_text).hexdigest()
            #output += hash_val
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
        else:
            form = HashForm()
    return render_to_response("hash_algo.html", {'algo' : algo_object,
                                            'hashvalue' : output,
                                            'hash' : hash_val,
                                            'clear_text' : clear_text,
                                            'form' : form,
                                            'algo_type' : 'Hash-Algorihmen',
                                            'manual' : manual,}) 
