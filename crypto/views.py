# encoding: utf-8
from crypt_app.crypto.models import AESEncryptForm, AESDecryptForm, SimpleEncryptForm, SimpleDecryptForm, RSAEncryptForm, RSADecryptForm, SimplestForm, CaesarEncryptForm, CaesarDecryptForm, AffineEncryptForm, AffineDecryptForm
from crypt_app.base_app.models import Algo, ManPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader
from cryptinterface import *

def algo(request, algo):
    output = u""
    cypher = u""
    algo_object = get_object_or_404(Algo, shortTitle=algo)
    manual = get_object_or_404(ManPage, algo=algo_object)
    if request.method == 'POST':
        if "keygen" in request.POST:
            return keygen()

        # encrypt
        if "submit1" in request.POST:
            if algo == 'aes':
                cypherForm = AESEncryptForm(request.POST)
                decypherForm = AESDecryptForm()
                if cypherForm.is_valid():
                    output, cypher = aesEncrypt(request)
            elif algo == 'des':
                cypherForm = AESEncryptForm(request.POST)
                decypherForm = AESDecryptForm()
                if cypherForm.is_valid():
                    output, cypher = desEncrypt(request)
            elif algo == 'xor':
                cypherForm = SimpleEncryptForm(request.POST)
                decypherForm = SimpleDecryptForm()
                if cypherForm.is_valid():
                    output, cypher = xorEncrypt(request)
            elif algo == 'rsa':
                cypherForm = RSAEncryptForm(request.POST, request.FILES)
                decypherForm = RSADecryptForm()
                if cypherForm.is_valid():
                    output, cypher = rsaEncrypt(request)
            elif algo == 'atbasch':
                cypherForm = SimplestForm(request.POST)
                decypherForm = None
                if cypherForm.is_valid():
                    output, cypher = atbaschEncrypt(request)
            elif algo == 'caesar':
                cypherForm = CaesarEncryptForm(request.POST)
                decypherForm = CaesarDecryptForm()
                if cypherForm.is_valid():
                    output, cypher = caesarEncrypt(request)
            elif algo == 'affine':
                cypherForm = AffineEncryptForm(request.POST)
                decypherForm = AffineDecryptForm()
                if cypherForm.is_valid():
                    output, cypher = affineEncrypt(request)
            else:
                output += u"Ungültiger Algorithmus"
        # decrypt
        elif "submit2" in request.POST:
            if algo == 'aes':
                cypherForm = AESEncryptForm()
                decypherForm = AESDecryptForm(request.POST)
                if decypherForm.is_valid():
                    cypher = aesDecrypt(request)
            elif algo == 'des':
                cypherForm = AESEncryptForm()
                decypherForm = AESDecryptForm(request.POST)
                if decypherForm.is_valid():
                    cypher = desDecrypt(request)
            elif algo == 'xor':
                cypherForm = SimpleEncryptForm()
                decypherForm = SimpleDecryptForm(request.POST)
                if decypherForm.is_valid():
                    cypher = xorDecrypt(request)   
            elif algo == 'rsa':
                cypherForm = RSAEncryptForm()
                decypherForm = RSADecryptForm(request.POST, request.FILES)
                if decypherForm.is_valid():
                    cypher = rsaDecrypt(request)
            elif algo == 'caesar':
                cypherForm = CaesarEncryptForm()
                decypherForm = CaesarDecryptForm(request.POST)
                if decypherForm.is_valid():
                    cypher = caesarDecrypt(request)
            elif algo == 'affine':
                cypherForm = AffineEncryptForm()
                decypherForm = AffineDecryptForm(request.POST)
                if decypherForm.is_valid():
                    cypher = affineDecrypt(request)
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


