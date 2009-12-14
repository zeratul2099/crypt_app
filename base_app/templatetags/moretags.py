# encoding: utf-8
from django import template


def umlauts(var):
    var = var.replace(u"ü", u"&uuml;")
    var = var.replace(u"Ü", u"&Uuml;")
    var = var.replace(u"ä", u"&auml;")
    var = var.replace(u"Ä", u"&Auml;")
    var = var.replace(u"ö", u"&ouml;")
    var = var.replace(u"Ö", u"&ouml;")
    var = var.replace(u"ß", u"&szlig;")
    return var

umlauts.is_safe = True
register = template.Library()
register.filter('umlauts', umlauts)
