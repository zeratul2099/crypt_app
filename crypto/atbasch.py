#!/usr/bin/env python


def atbasch(cleartext):
    cypher = ""
    num = 0
    for letter in cleartext.lower():
        num = 25-(ord(letter)-97)
        if 0 <= num < 26:
            cypher+=chr(num+97)
    return cypher

