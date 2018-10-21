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

from crypto.models import AESEncryptForm, AESDecryptForm, SimpleEncryptForm, SimpleDecryptForm, RSAEncryptForm, RSADecryptForm, SimplestForm, CaesarEncryptForm, CaesarDecryptForm, AffineEncryptForm, AffineDecryptForm
from base_app.models import Algo, ManPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader
from crypto.cryptointerface import *

def algo(request, algo):
    output = ""
    cypher = ""
    algo_object = get_object_or_404(Algo, shortTitle=algo)
    manual = get_object_or_404(ManPage, algo=algo_object)
    
    cypherFormDict = { 'aes' : AESEncryptForm,
                       'des' : AESEncryptForm,
                       'xor' : SimpleEncryptForm,
                       'rsa' : RSAEncryptForm,
                       'atbasch' : SimplestForm,
                       'caesar' : CaesarEncryptForm,
                       'affine' : AffineEncryptForm, }
                
    decypherFormDict = { 'aes' : AESDecryptForm,
                       'des' : AESDecryptForm,
                       'xor' : SimpleDecryptForm,
                       'rsa' : RSADecryptForm,
                       'atbasch' : None,
                       'caesar' : CaesarDecryptForm,
                       'affine' : AffineDecryptForm, }
    
    
    if request.method == 'POST':
                        
        if "keygen" in request.POST:
            return keygen()

        # encrypt
        elif "submit1" in request.POST:
            algoDict = {'aes' : aesEncrypt,
                        'des' : desEncrypt,
                        'xor' : xorEncrypt,
                        'rsa' : rsaEncrypt,
                        'atbasch' : atbaschEncrypt,
                        'caesar' : caesarEncrypt,
                        'affine' : affineEncrypt, }

            cypherForm = cypherFormDict[algo](request.POST)
            if decypherFormDict[algo]:
                decypherForm = decypherFormDict[algo]()
            else:
                decypherForm = None
            if cypherForm.is_valid():
                output, cypher = algoDict[algo](request)
            
        # decrypt
        elif "submit2" in request.POST:
            
            algoDict = {'aes' : aesDecrypt,
                        'des' : desDecrypt,
                        'xor' : xorDecrypt,
                        'rsa' : rsaDecrypt,
                        'caesar' : caesarDecrypt,
                        'affine' : affineDecrypt, }
            cypherForm = cypherFormDict[algo]()
            decypherForm = decypherFormDict[algo](request.POST)
            if decypherForm.is_valid():
                cypher = algoDict[algo](request)
                
    else:
        cypherForm = cypherFormDict[algo]()
        if decypherFormDict[algo]:
            decypherForm = decypherFormDict[algo]()
        else:
            decypherForm = None

    return render_to_response("crypto_algo.html", {'algo' : algo_object,
                                            'output' : output,
                                            'cypher' : cypher,
                                            'decypherForm' : decypherForm, 
                                            'cypherForm' : cypherForm,
                                            'algo_type' : 'Kryptographie',
                                            'manual' : manual,}) 


