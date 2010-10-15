# -*- coding: utf-8 -*-
from django import template

def umlauts(var):
    var = var.replace(u"ü", u"&uuml;")
    var = var.replace(u"Ü", u"&Uuml;")
    var = var.replace(u"ä", u"&auml;")
    var = var.replace(u"Ä", u"&Auml;")
    var = var.replace(u"ë", u"&euml;")
    var = var.replace(u"Ë", u"&Euml;")
    var = var.replace(u"ö", u"&ouml;")
    var = var.replace(u"Ö", u"&Ouml;")
    var = var.replace(u"ø", u"&oslash;")
    var = var.replace(u"Ø", u"&Oslash;")
    var = var.replace(u"á", u"&aacute;")
    var = var.replace(u"Á", u"&Aacute;")
    var = var.replace(u"é", u"&eacute;")
    var = var.replace(u"É", u"&Eacute;")
    var = var.replace(u"í", u"&iacute;")
    var = var.replace(u"Í", u"&Iacute;")
    var = var.replace(u"ó", u"&Iocute;")
    var = var.replace(u"Ó", u"&Oacute;")
    var = var.replace(u"ú", u"&uacute;")
    var = var.replace(u"Ú", u"&Uacute;")
    var = var.replace(u"ý", u"&yacute;")
    var = var.replace(u"Ý", u"&Yacute;")
    var = var.replace(u"à", u"&agrave;")
    var = var.replace(u"À", u"&Agrave;")
    var = var.replace(u"è", u"&egrave;")
    var = var.replace(u"È", u"&Egrave;")
    var = var.replace(u"ì", u"&igrave;")
    var = var.replace(u"Ì", u"&Igrave;")
    var = var.replace(u"ò", u"&ograve;")
    var = var.replace(u"Ò", u"&Ograve;")
    var = var.replace(u"ù", u"&ugrave;")
    var = var.replace(u"Ù", u"&Ugrave;")
    var = var.replace(u"ß", u"&szlig;")
    var = var.replace(u"ç", u"&ccedil;")
    var = var.replace(u"Ç", u"&Ccedil;")
    print var;
    return var

def setIcon(var):
  if var == "message" or var == "clear":
    var = "<img width='16' height='16' border='0' src='/content/icons/txt.png' ></img>"
  elif var == "key" or var == "keyA" or var == "keyB" or var == "pw":
    var = "<img width='16' height='16' border='0' src='/content/icons/key.png' ></img>"
  elif var == "cypher_text":
    var = "<img width='16' height='16' border='0' src='/content/icons/encrypted.png' ></img>"
  elif var == "block_mode" or var == "width" or var == "height":
    var = "<img width='16' height='16' border='0' src='/content/icons/blocks.png' ></img>"    
  elif var == "file":
    var = "<img width='16' height='16' border='0' src='/content/icons/image.png' ></img>"
  elif var == "fileH":
    var = "<img width='16' height='16' border='0' src='/content/icons/file.png' ></img>"
  elif var == "withSalt":
    var = "<img width='16' height='16' border='0' src='/content/icons/add.png' ></img>"  
  else:
    var = "<img width='16' height='16' border='0' src='/content/icons/empty.png' ></img>"      
  return(var)


umlauts.is_safe = True
setIcon.is_safe = True
register = template.Library()
register.filter('umlauts', umlauts)
register.filter('setIcon', setIcon)
