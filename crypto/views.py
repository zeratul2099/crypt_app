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

from django.shortcuts import get_object_or_404, render_to_response

from .models import (
    AESEncryptForm,
    AESDecryptForm,
    SimpleEncryptForm,
    SimpleDecryptForm,
    RSAEncryptForm,
    RSADecryptForm,
    SimplestForm,
    CaesarEncryptForm,
    CaesarDecryptForm,
    AffineEncryptForm,
    AffineDecryptForm,
)
from .cryptointerface import (
    desEncrypt,
    desDecrypt,
    aesEncrypt,
    aesDecrypt,
    rsaEncrypt,
    rsaDecrypt,
    xorEncrypt,
    xorDecrypt,
    atbaschEncrypt,
    caesarEncrypt,
    caesarDecrypt,
    affineEncrypt,
    affineDecrypt,
    keygen,
)
from base_app.models import Algo, ManPage


def algo(request, algo_name):
    output = ""
    cypher = ""
    algo_object = get_object_or_404(Algo, shortTitle=algo_name)
    manual = get_object_or_404(ManPage, algo=algo_object)

    cypherFormDict = {
        "aes": AESEncryptForm,
        "des": AESEncryptForm,
        "xor": SimpleEncryptForm,
        "rsa": RSAEncryptForm,
        "atbasch": SimplestForm,
        "caesar": CaesarEncryptForm,
        "affine": AffineEncryptForm,
    }

    decypherFormDict = {
        "aes": AESDecryptForm,
        "des": AESDecryptForm,
        "xor": SimpleDecryptForm,
        "rsa": RSADecryptForm,
        "atbasch": None,
        "caesar": CaesarDecryptForm,
        "affine": AffineDecryptForm,
    }

    if request.method == "POST":

        if "keygen" in request.POST:
            return keygen()

        # encrypt
        elif "submit1" in request.POST:
            algoDict = {
                "aes": aesEncrypt,
                "des": desEncrypt,
                "xor": xorEncrypt,
                "rsa": rsaEncrypt,
                "atbasch": atbaschEncrypt,
                "caesar": caesarEncrypt,
                "affine": affineEncrypt,
            }

            cypherForm = cypherFormDict[algo_name](request.POST)
            if decypherFormDict[algo_name]:
                decypherForm = decypherFormDict[algo_name]()
            else:
                decypherForm = None
            if cypherForm.is_valid():
                output, cypher = algoDict[algo_name](request)

        # decrypt
        elif "submit2" in request.POST:

            algoDict = {
                "aes": aesDecrypt,
                "des": desDecrypt,
                "xor": xorDecrypt,
                "rsa": rsaDecrypt,
                "caesar": caesarDecrypt,
                "affine": affineDecrypt,
            }
            cypherForm = cypherFormDict[algo_name]()
            decypherForm = decypherFormDict[algo_name](request.POST)
            if decypherForm.is_valid():
                cypher = algoDict[algo_name](request)

    else:
        cypherForm = cypherFormDict[algo_name]()
        if decypherFormDict[algo_name]:
            decypherForm = decypherFormDict[algo_name]()
        else:
            decypherForm = None

    return render_to_response(
        "crypto_algo.html",
        {
            "algo": algo_object,
            "output": output,
            "cypher": cypher,
            "decypherForm": decypherForm,
            "cypherForm": cypherForm,
            "algo_type": "Kryptographie",
            "manual": manual,
        },
    )
