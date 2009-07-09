from crypt_app.hashtest.models import HashForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader
from KezzakHash import KezzakHash
import hashlib


def hashtest(request):
    if request.method == 'POST':
        form = HashForm(request.POST, request.FILES)
        if request.FILES:
            clear_text = request.FILES['file'].read()
            output = "Input file:\n%s (%s Bytes)\n" %(request.FILES['file'].name,
                                                      request.FILES['file'].size)
        else:
            clear_text = request.POST.get("clear", "")
            output = "Input string:\n%s\n" %(clear_text)
            
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
        elif request.POST.get("algorithm", "") == 'kezzak':
            output += "Kezzak[800]-Hash:\n"
            output += KezzakHash(repr(clear_text)).hexdigest()
    else:
        clear_text = ""
        output = 'Spam'
        form = HashForm()
        #hashes = {'md5' : 'MD5', 'sha1' : 'SHA-1'}
        #form.algorithm(hashes)
    return render_to_response("hash.html", {'hashvalue' : output, 'clear_text' : clear_text, 'form' : form})      
        
    
