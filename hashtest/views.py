from crypt_app.hashtest.models import HashForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader
from KeccakHash import KeccakHash
from datetime import datetime
import hashlib, random, sys


def hashtest(request):
    salt = 0
    salt_str = ''
    if request.method == 'POST':
        
        if request.FILES:
            if request.FILES['file'].size > 10000:
                form = HashForm()
                return render_to_response("hash.html", {'hashvalue' : 'Datei zu gross',  'form' : form}) 
            clear_text = request.FILES['file'].read()
            output = "Eingabedatei:\n%s (%s Bytes)\n" %(request.FILES['file'].name,
                                                      request.FILES['file'].size)
        else:
            clear_text = request.POST.get("clear", "")
            output = "Eingabestring:\n%s\n" %(clear_text)
            
        if 'withSalt' in request.POST:
            rand = random.Random(datetime.now().strftime('%s'))
            salt = rand.randint(0, sys.maxint)
            for i in range(4):
                salt_str += chr((salt%(1<<(8*(i+1))))>>((i*8)+1))
            clear_text += salt_str
            
        form = HashForm(request.POST, request.FILES)   
        if request.POST.get("algorithm", "") == 'md5':
            output += "MD5-Hash:\n"
            output += hashlib.md5(clear_text).hexdigest()
        elif request.POST.get("algorithm", "") == 'sha1':
            output += "SHA-1-Hash:\n"
            output += hashlib.sha1(clear_text).hexdigest()
        elif request.POST.get("algorithm", "") == 'sha224':
            output += "SHA-224-Hash:\n"
            output += hashlib.sha224(clear_text).hexdigest()
        elif request.POST.get("algorithm", "") == 'sha256':
            output += "SHA-256-Hash:\n"
            output += hashlib.sha256(clear_text).hexdigest()
        elif request.POST.get("algorithm", "") == 'sha384':
            output += "SHA-384-Hash:\n"
            output += hashlib.sha384(clear_text).hexdigest()
        elif request.POST.get("algorithm", "") == 'sha512':
            output += "SHA-512-Hash:\n"
            output += hashlib.sha512(clear_text).hexdigest()
        elif request.POST.get("algorithm", "") == 'keccak':
            output += "Keccak[800]-224-Hash:\n"
            output += KeccakHash(repr(clear_text)).hexdigest()
        
        if 'withSalt' in request.POST:
            output += "\nSalt:\n"
            output += repr(salt_str)
    else:
        clear_text = ""
        output = ''
        form = HashForm()
        #hashes = {'md5' : 'MD5', 'sha1' : 'SHA-1'}
        #form.algorithm(hashes)
    return render_to_response("hash.html", {'hashvalue' : output,
                                            'clear_text' : clear_text,
                                            'form' : form,})      
        
    
