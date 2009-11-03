from crypt_app.crypto.models import AESEncryptForm, AESDecryptForm
from crypt_app.base_app.models import Algo
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader
from Crypto.Cipher import AES
from Crypto.Util import RFC1751 as rfc
from Crypto.Util import number

def algo(request, algo):
    output = ""
    cypher = ""
    algo_object = get_object_or_404(Algo, shortTitle=algo)
    if request.method == 'POST':


        # encrypt
        if "submit1" in request.POST:
            plain_text = request.POST["message"]
            if algo == 'aes':
                cypherForm = AESEncryptForm(request.POST)
                decypherForm = AESDecryptForm()
                if cypherForm.is_valid():
                    extend = 16 - (len(plain_text) % 16)
                    for i in range(extend):
                        plain_text += "X"
                    output = "Klartext (erweitert):\n%s\n\n" %(plain_text)
                    key = number.long_to_bytes(request.POST["key"], 16)[0:32]
                    output += "Key: %s\n\n"%(request.POST["key"])
                    output += "AES-verschluesselt:\n"
                    aesObject = AES.new(key, int(request.POST["block_mode"]))
                    cypher = number.bytes_to_long(aesObject.encrypt(plain_text))
            else:
                output += "Invalid algorithm"
        # decrypt
        elif "submit2" in request.POST:
            if algo == 'aes':
                cypherForm = AESEncryptForm()
                decypherForm = AESDecryptForm(request.POST)
                if decypherForm.is_valid():
                    key = number.long_to_bytes(request.POST["key"], 16)[0:32]
                    output = "Klartext:\n"
                    aesObject = AES.new(key, int(request.POST["block_mode"]))
                    cypher = aesObject.decrypt(number.long_to_bytes(request.POST["cypher_text"]))
    else:
        cypherForm = AESEncryptForm()
        decypherForm = AESDecryptForm()
    
    return render_to_response("crypto_algo.html", {'title' : algo_object.name,
                                            'algo' : algo,
                                            'output' : output,
                                            'cypher' : cypher,
                                            'decypherForm' : decypherForm, 
                                            'cypherForm' : cypherForm,}) 
