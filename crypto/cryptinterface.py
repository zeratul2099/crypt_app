# encoding: utf-8
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from Crypto.Cipher import AES, DES, XOR
from Crypto.Util import number
from M2Crypto import RSA
from classic import *
import zipfile, os


def keygen():
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


def aesEncrypt(request):
    plain_text = request.POST["message"]
    extend = 16 - (len(plain_text) % 16)
    for i in range(extend):
        plain_text += "X"
    output = u"Klartext (erweitert):\n%s\n\n" %(plain_text)
    key = number.long_to_bytes(request.POST["key"], 16)[0:32]
    output += u"Schlüssel: %s\n\n"%(request.POST["key"])
    output += u"AES-verschlüsselt:\n"
    aesObject = AES.new(key, int(request.POST["block_mode"]))
    cypher = number.bytes_to_long(aesObject.encrypt(plain_text))
    return ( output, cypher )

def desEncrypt(request):
    plain_text = request.POST["message"]
    extend = 8 - (len(plain_text) % 8)
    for i in range(extend):
        plain_text += "X"
    output = u"Klartext (erweitert):\n%s\n\n" %(plain_text)
    key = number.long_to_bytes(request.POST["key"], 8)[0:8]
    output += u"Schlüssel: %s\n\n"%(request.POST["key"])
    output += u"DES-verschlüsselt:\n"
    desObject = DES.new(key, int(request.POST["block_mode"]))
    cypher = number.bytes_to_long(desObject.encrypt(plain_text))
    return ( output, cypher )
    
def xorEncrypt(request):
    plain_text = request.POST["message"]
    output = u"Klartext:\n%s\n\n" %(plain_text)
    key = number.long_to_bytes(request.POST["key"], 0)
    output += u"Schlüssel: %s\n\n"%(request.POST["key"])
    output += u"XOR-verschlüsselt:\n"
    xorObject = XOR.new(key)
    cypher = number.bytes_to_long(xorObject.encrypt(plain_text))
    return ( output, cypher )
    
def rsaEncrypt(request):
    plain_text = request.POST["message"]
    output = u"Klartext:\n%s\n\n" %(plain_text)
    output += u"RSA-verschlüsselt:\n"
    try:
        PubKey = RSA.load_pub_key(request.FILES['key'].temporary_file_path())
        cypher = number.bytes_to_long(PubKey.public_encrypt(plain_text, 1))
    except RSA.RSAError, e:
        output = str(e)
        cypher = ""
    return ( output, cypher )
    
def atbaschEncrypt(request):
    plain_text = request.POST["message"]
    output = u"Klartext:\n%s\n\n" %(plain_text)
    output += u"Atbasch-verschlüsselt:\n"
    cypher = atbasch(plain_text)
    return ( output, cypher )
    
    
def caesarEncrypt(request):
    plain_text = request.POST["message"]
    output = u"Klartext:\n%s\n\n" %(plain_text)
    output += u"ROT%s-verschlüsselt:\n"%(request.POST["key"])
    cypher = caesar(plain_text, int(request.POST["key"]), True)
    return ( output, cypher )
    
def affineEncrypt(request):
    plain_text = request.POST["message"]
    output = u"Klartext:\n%s\n\n" %(plain_text)
    output += u"(%s, %s)-verschlüsselt:\n"%(request.POST["keyA"], request.POST["keyB"])
    cypher = affineEnc(plain_text, int(request.POST["keyA"]), int(request.POST["keyB"]))
    return ( output, cypher )
    
def aesDecrypt(request):
    key = number.long_to_bytes(request.POST["key"], 16)[0:32]
    aesObject = AES.new(key, int(request.POST["block_mode"]))
    return aesObject.decrypt(number.long_to_bytes(request.POST["cypher_text"]))
    
def desDecrypt(request):
    key = number.long_to_bytes(request.POST["key"], 8)[0:8]
    desObject = DES.new(key, int(request.POST["block_mode"]))
    return desObject.decrypt(number.long_to_bytes(request.POST["cypher_text"])) 
    
def xorDecrypt(request):
    key = number.long_to_bytes(request.POST["key"], 0)
    xorObject = XOR.new(key)
    return xorObject.decrypt(number.long_to_bytes(request.POST["cypher_text"])) 
    
def rsaDecrypt(request):
    try:
        PrivKey = RSA.load_key(request.FILES['key'].temporary_file_path())
        return PrivKey.private_decrypt(number.long_to_bytes(request.POST["cypher_text"]), 1).replace('\0','')
    except RSA.RSAError, e:
        return str(e)
    
def caesarDecrypt(request):
    return caesar(request.POST["cypher_text"], int(request.POST['key']), False)
    
def affineDecrypt(request):
    return affineDec(request.POST["cypher_text"], int(request.POST['keyA']), int(request.POST['keyB']))

