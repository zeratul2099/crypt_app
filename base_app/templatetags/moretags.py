# -*- coding: utf-8 -*-
from django import template

def umlauts(var):
    var = var.replace("ü", "&uuml;")
    var = var.replace("Ü", "&Uuml;")
    var = var.replace("ä", "&auml;")
    var = var.replace("Ä", "&Auml;")
    var = var.replace("ë", "&euml;")
    var = var.replace("Ë", "&Euml;")
    var = var.replace("ö", "&ouml;")
    var = var.replace("Ö", "&Ouml;")
    var = var.replace("ø", "&oslash;")
    var = var.replace("Ø", "&Oslash;")
    var = var.replace("á", "&aacute;")
    var = var.replace("Á", "&Aacute;")
    var = var.replace("é", "&eacute;")
    var = var.replace("É", "&Eacute;")
    var = var.replace("í", "&iacute;")
    var = var.replace("Í", "&Iacute;")
    var = var.replace("ó", "&Iocute;")
    var = var.replace("Ó", "&Oacute;")
    var = var.replace("ú", "&uacute;")
    var = var.replace("Ú", "&Uacute;")
    var = var.replace("ý", "&yacute;")
    var = var.replace("Ý", "&Yacute;")
    var = var.replace("à", "&agrave;")
    var = var.replace("À", "&Agrave;")
    var = var.replace("è", "&egrave;")
    var = var.replace("È", "&Egrave;")
    var = var.replace("ì", "&igrave;")
    var = var.replace("Ì", "&Igrave;")
    var = var.replace("ò", "&ograve;")
    var = var.replace("Ò", "&Ograve;")
    var = var.replace("ù", "&ugrave;")
    var = var.replace("Ù", "&Ugrave;")
    var = var.replace("ß", "&szlig;")
    var = var.replace("ç", "&ccedil;")
    var = var.replace("Ç", "&Ccedil;")
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
