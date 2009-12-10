#!/usr/bin/env python

def atbasch(cleartext):
    cypher = ""
    num = 0
    for letter in cleartext.lower():
        num = 25-(ord(letter)-97)
        if 0 <= num < 26:
            cypher+=chr(num+97)
        elif num == 90:
            cypher+= " "
    return cypher


def caesar(cleartext, shift, encrypt):
    cypher = ""
    num = 0
    for letter in cleartext.lower():
        if 97 <= ord(letter) <= 122:
            if encrypt:
                num = ((ord(letter)-97)+shift) % 26
            else:
                num = ((ord(letter)-97)-shift) % 26
        #if 0 <= num < 26:
            cypher+=chr(num+97)
        elif ord(letter) == 32:
            cypher+= " "
    return cypher

def affineEnc(cleartext, a, b):
    cypher = ""
    num = 0
    for letter in cleartext.lower():
        if 97 <= ord(letter) <= 122:
            num = (a*((ord(letter)-97)+b)) % 26
            cypher+=chr(num+97)
        elif ord(letter) == 32:
            cypher+= " "
    return cypher

def affineDec(cypher, a, b):
    cleartext = ""
    num = 0
    for letter in cypher.lower():
        if 97 <= ord(letter) <= 122:
            num = (((ord(letter)-97)-b)/a) % 26
            cleartext+=chr(num+97)
        elif ord(letter) == 32:
            cleartext+= " "
    return cleartext