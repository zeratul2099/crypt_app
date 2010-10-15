# encoding: utf-8
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


from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from Crypto.Cipher import AES, DES, XOR
from Crypto.Util import number
from M2Crypto import RSA
from classic import *
import zipfile, os
import hashlib

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
    print "call"
    plain_text = request.POST["message"]
    extend = 16 - (len(plain_text) % 16)
    for i in range(extend):
        plain_text += "X"
    output = u"Klartext (erweitert):\n%s\n\n" %(plain_text)
    key = hashlib.sha256(request.POST["key"]).digest()
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
    key = hashlib.sha256(request.POST["key"]).digest()[0:8]
    output += u"Schlüssel: %s\n\n"%(request.POST["key"])
    output += u"DES-verschlüsselt:\n"
    desObject = DES.new(key, int(request.POST["block_mode"]))
    cypher = number.bytes_to_long(desObject.encrypt(plain_text))
    return ( output, cypher )
    
def xorEncrypt(request):
    plain_text = request.POST["message"]
    output = u"Klartext:\n%s\n\n" %(plain_text)
    key = hashlib.sha256(request.POST["key"]).digest()
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
    key = hashlib.sha256(request.POST["key"]).digest()
    aesObject = AES.new(key, int(request.POST["block_mode"]))
    return aesObject.decrypt(number.long_to_bytes(request.POST["cypher_text"]))
    
def desDecrypt(request):
    key = hashlib.sha256(request.POST["key"]).digest()[0:8]
    desObject = DES.new(key, int(request.POST["block_mode"]))
    return desObject.decrypt(number.long_to_bytes(request.POST["cypher_text"])) 
    
def xorDecrypt(request):
    key = hashlib.sha256(request.POST["key"]).digest()
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

