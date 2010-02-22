# encoding: utf-8
from crypt_app.stego.models import CPTEmbedForm, CPTExtractForm
from crypt_app.stego.models import F5EmbedForm, F5ExtractForm
from crypt_app.stego.models import LsbEmbedForm, LsbExtractForm
from crypt_app.stego.models import GifShuffleEmbedForm, GifShuffleExtractForm
from crypt_app.stego.models import BattlestegEmbedForm, BattlestegExtractForm
from crypt_app.base_app.models import Algo, InfoPage, ManPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader
from django.core.servers.basehttp import FileWrapper
try:
    from processing import Process, Pipe, Queue
except ImportError:
    from multiprocessing import Process, Pipe, Queue as Q

import Queue as Q
import os
from stegointerface import *

def algo(request, algo):
    text = ""
    type = ""
    algo_object = get_object_or_404(Algo, shortTitle=algo)
    manual = get_object_or_404(ManPage, algo=algo_object)
    
    embedFormDict = { 'cpt' : CPTEmbedForm,
                   'f5' : F5EmbedForm,
                   'lsb' : LsbEmbedForm,
                   'gifshuffle' : GifShuffleEmbedForm,
                   'bs' : BattlestegEmbedForm, }
    
    extractFormDict = { 'cpt' : CPTExtractForm,
                   'f5' : F5ExtractForm,
                   'lsb' : LsbExtractForm,
                   'gifshuffle' : GifShuffleExtractForm,
                   'bs' : BattlestegExtractForm, }
    typeDict = { 'cpt' : "png",
               'f5' : "jpeg",
               'lsb' : "png",
               'gifshuffle' : "gif",
               'bs' : "png", }
    
    if request.method == 'POST':
        
        q = Queue()
        # embedding
        if "submit1" in request.POST:
            
            algoDict = { 'cpt' : cptEmbed,
                           'f5' : f5Embed,
                           'lsb' : lsbEmbed,
                           'gifshuffle' : gifShuffleEmbed,
                           'bs' : bsEmbed, }
            
            embedForm = embedFormDict[algo](request.POST, request.FILES)
            extractForm = extractFormDict[algo]()
            type = typeDict[algo]
            p = Process(target=algoDict[algo], args=(q, ))

            # fork process to embed
            if embedForm.is_valid():
                p.start()
                q.put([request.POST, request.FILES['file'].temporary_file_path()])
                os.system("sleep 1")
                try:
                    retval = q.get(True, 10)
                except Q.Empty:
                    retval = -2
                p.join()
                if retval == -1:
                    text += "%s-Datei nicht gefunden oder fehlerhaft."%(type)
                elif retval == -2:
                    text += "Fehler beim Einbetten. Anderes Bild oder andere Parameter versuchen."
                else:
                    return createResponse(retval, type)
        # extracting        
        elif "submit2" in request.POST:
             
            algoDict = { 'cpt' : cptExtract,
                           'f5' : f5Extract,
                           'lsb' : lsbExtract,
                           'gifshuffle' : gifShuffleExtract,
                           'bs' : bsExtract, }

            embedForm = embedFormDict[algo]()
            extractForm = extractFormDict[algo](request.POST, request.FILES)
            type = typeDict[algo]
            p = Process(target=algoDict[algo], args=(q, ))
            
            # fork process to extract
            if extractForm.is_valid():
                p.start()
                q.put([request.POST, request.FILES['file'].temporary_file_path()])
                try:
                    retval = q.get(True, 10)
                except Q.Empty:
                    retval = -2
                p.join()
                if retval == -1:
                    text += "%s-Datei nicht gefunden oder fehlerhaft."%(type)
                elif retval == -2:
                    text += "Fehler beim Ausbetten. Anderes Bild oder andere Parameter versuchen."
                else:
                    text += retval
    # empty form
    else:
        embedForm = embedFormDict[algo]()
        extractForm = extractFormDict[algo]()
    # render
    return render_to_response("stego_algo.html", {'algo' : algo_object,
                                            'embedForm' : embedForm, 
                                            'extractForm' : extractForm,
                                            'text' : text,
                                            'algo_type' : 'Staganographie',
                                            'manual' : manual,}) 

def createResponse(filename, type):
    wrapper = FileWrapper(file(filename))

    response = HttpResponse(wrapper, mimetype='image/%s'%(type))
    response['Content-Length'] = os.path.getsize(filename)

    response['Content-Disposition'] = 'attachment; filename=stego.%s'%(type)
    return response

    

