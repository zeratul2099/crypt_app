# encoding: utf-8
from crypt_app.crypto.models import AESEncryptForm, AESDecryptForm, SimpleEncryptForm, SimpleDecryptForm, RSAEncryptForm, RSADecryptForm, SimplestForm, CaesarEncryptForm, CaesarDecryptForm, AffineEncryptForm, AffineDecryptForm
from crypt_app.base_app.models import Algo, ManPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader
from django.core.servers.basehttp import FileWrapper
from Crypto.Cipher import AES, DES, XOR
from Crypto.Util import number
from M2Crypto import RSA
from classic import atbasch, caesar, affineEnc, affineDec
import zipfile, os

def algo(request, algo):
    output = u""
    cypher = u""
    algo_object = get_object_or_404(Algo, shortTitle=algo)
    manual = get_object_or_404(ManPage, algo=algo_object)
    if request.method == 'POST':
        if "keygen" in request.POST:
            RSAKey = RSA.gen_key(2048, 1023)
            RSAKey.save_key("private.pem",cipher=None)
            RSAKey.save_pub_key("public.pem")
            zipF = zipfile.ZipFile("keys.zip", "w")
            zipF.write("private.pem")
            zipF.write("public.pem")
            zipF.close()
            os.remove("private.pem")
            os.remove("public.pem")
            wrapper = FileWrapper(file("keys.zip"))
            response = HttpResponse(wrapper, mimetype='application/zip')
            response['Content-Length'] = os.path.getsize("keys.zip")
            response['Content-Disposition'] = 'attachment; filename=keys.zip'
            os.remove("keys.zip")
            return response

        # encrypt
        if "submit1" in request.POST:
            plain_text = u""
            plain_text = request.POST["message"]
            plain_text = plain_text
            if algo == 'aes':
                cypherForm = AESEncryptForm(request.POST)
                decypherForm = AESDecryptForm()
                if cypherForm.is_valid():
                    extend = 16 - (len(plain_text) % 16)
                    for i in range(extend):
                        plain_text += "X"
                    #plain_text = plain_text.encode("utf-8")
                    #output = u"Klartext (erweitert):\n%s\n\n" %(plain_text)
                    key = number.long_to_bytes(request.POST["key"], 16)[0:32]
                    output += u"Schlüssel: %s\n\n"%(request.POST["key"])
                    output += u"AES-verschlüsselt:\n"
                    aesObject = AES.new(key, int(request.POST["block_mode"]))
                    cypher = number.bytes_to_long(aesObject.encrypt(plain_text))
            elif algo == 'des':
                cypherForm = AESEncryptForm(request.POST)
                decypherForm = AESDecryptForm()
                if cypherForm.is_valid():
                    extend = 8 - (len(plain_text) % 8)
                    for i in range(extend):
                        plain_text += "X"
                    output = u"Klartext (erweitert):\n%s\n\n" %(plain_text)
                    key = number.long_to_bytes(request.POST["key"], 8)[0:8]
                    output += u"Schlüssel: %s\n\n"%(request.POST["key"])
                    output += u"DES-verschlüsselt:\n"
                    desObject = DES.new(key, int(request.POST["block_mode"]))
                    cypher = number.bytes_to_long(desObject.encrypt(plain_text))

            elif algo == 'xor':
                cypherForm = SimpleEncryptForm(request.POST)
                decypherForm = SimpleDecryptForm()
                if cypherForm.is_valid():
                    output = u"Klartext:\n%s\n\n" %(plain_text)
                    key = number.long_to_bytes(request.POST["key"], 0)
                    output += u"Schlüssel: %s\n\n"%(request.POST["key"])
                    output += u"XOR-verschlüsselt:\n"
                    xorObject = XOR.new(key)
                    cypher = number.bytes_to_long(xorObject.encrypt(plain_text))
            elif algo == 'rsa':
                cypherForm = RSAEncryptForm(request.POST, request.FILES)
                decypherForm = RSADecryptForm()
                if cypherForm.is_valid():
                    output = u"Klartext:\n%s\n\n" %(plain_text)
                    output += u"RSA-verschlüsselt:\n"
                    try:
                        PubKey = RSA.load_pub_key(request.FILES['key'].temporary_file_path())
                        cypher = number.bytes_to_long(PubKey.public_encrypt(plain_text, 1))
                    except RSA.RSAError, e:
                        output = e
            elif algo == 'atbasch':
                cypherForm = SimplestForm(request.POST)
                decypherForm = None
                if cypherForm.is_valid():
                    output = u"Klartext:\n%s\n\n" %(plain_text)
                    output += u"Atbasch-verschlüsselt:\n"
                    cypher = atbasch(plain_text)
            elif algo == 'caesar':
                cypherForm = CaesarEncryptForm(request.POST)
                decypherForm = CaesarDecryptForm()
                if cypherForm.is_valid():
                    output = u"Klartext:\n%s\n\n" %(plain_text)
                    output += u"ROT%s-verschlüsselt:\n"%(request.POST["key"])
                    cypher = caesar(plain_text, int(request.POST["key"]), True)
            elif algo == 'affine':
                cypherForm = AffineEncryptForm(request.POST)
                decypherForm = AffineDecryptForm()
                if cypherForm.is_valid():
                    output = u"Klartext:\n%s\n\n" %(plain_text)
                    output += u"(%s, %s)-verschlüsselt:\n"%(request.POST["keyA"], request.POST["keyB"])
                    cypher = affineEnc(plain_text, int(request.POST["keyA"]), int(request.POST["keyB"]))
            else:
                output += u"Ungültiger Algorithmus"
        # decrypt
        elif "submit2" in request.POST:
            if algo == 'aes':
                cypherForm = AESEncryptForm()
                decypherForm = AESDecryptForm(request.POST)
                if decypherForm.is_valid():
                    key = number.long_to_bytes(request.POST["key"], 16)[0:32]
                    aesObject = AES.new(key, int(request.POST["block_mode"]))
                    cypher = aesObject.decrypt(number.long_to_bytes(request.POST["cypher_text"]))
            elif algo == 'des':
                cypherForm = AESEncryptForm()
                decypherForm = AESDecryptForm(request.POST)
                if decypherForm.is_valid():
                    key = number.long_to_bytes(request.POST["key"], 8)[0:8]
                    desObject = DES.new(key, int(request.POST["block_mode"]))
                    cypher = desObject.decrypt(number.long_to_bytes(request.POST["cypher_text"]))                
            elif algo == 'xor':
                cypherForm = SimpleEncryptForm()
                decypherForm = SimpleDecryptForm(request.POST)
                if decypherForm.is_valid():
                    key = number.long_to_bytes(request.POST["key"], 0)
                    xorObject = XOR.new(key)
                    cypher = xorObject.decrypt(number.long_to_bytes(request.POST["cypher_text"]))   
            elif algo == 'rsa':
                cypherForm = RSAEncryptForm()
                decypherForm = RSADecryptForm(request.POST, request.FILES)
                if decypherForm.is_valid():
                    try:
                        PrivKey = RSA.load_key(request.FILES['key'].temporary_file_path())
                        cypher = PrivKey.private_decrypt(number.long_to_bytes(request.POST["cypher_text"]), 1).replace('\0','')
                    except RSA.RSAError, e:
                        output = e
            elif algo == 'caesar':
                cypherForm = CaesarEncryptForm()
                decypherForm = CaesarDecryptForm(request.POST)
                if decypherForm.is_valid():
                    cypher = caesar(request.POST["cypher_text"], int(request.POST['key']), False)
            elif algo == 'affine':
                cypherForm = AffineEncryptForm()
                decypherForm = AffineDecryptForm(request.POST)
                if decypherForm.is_valid():
                    cypher = affineDec(request.POST["cypher_text"], int(request.POST['keyA']), int(request.POST['keyB']))
            else:
                output += "Invalid algorithm"
    else:
        if algo == 'aes' or algo == 'des':
            cypherForm = AESEncryptForm()
            decypherForm = AESDecryptForm()
        elif algo == 'xor':
            cypherForm = SimpleEncryptForm()
            decypherForm = SimpleDecryptForm()
        elif algo == 'rsa':
            cypherForm = RSAEncryptForm()
            decypherForm = RSADecryptForm()
        elif algo == 'atbasch':
            cypherForm = SimplestForm()
            decypherForm = None
        elif algo == 'caesar':
            cypherForm = CaesarEncryptForm()
            decypherForm = CaesarDecryptForm()
        elif algo == 'affine':
            cypherForm = AffineEncryptForm()
            decypherForm = AffineDecryptForm()

                
    return render_to_response("crypto_algo.html", {'algo' : algo_object,
                                            'output' : output,
                                            'cypher' : cypher,
                                            'decypherForm' : decypherForm, 
                                            'cypherForm' : cypherForm,
                                            'algo_type' : 'Kryptographie',
                                            'manual' : manual,}) 
