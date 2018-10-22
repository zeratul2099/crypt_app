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

import os
from queue import Queue
from multiprocessing import Process, Queue as Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.servers.basehttp import FileWrapper # pylint: disable=no-name-in-module
from .models import CPTEmbedForm, CPTExtractForm
from .models import F5EmbedForm, F5ExtractForm
from .models import LsbEmbedForm, LsbExtractForm
from .models import GifShuffleEmbedForm, GifShuffleExtractForm
from .models import BattlestegEmbedForm, BattlestegExtractForm
from base_app.models import Algo, ManPage

from .stegointerface import (
    cptEmbed,
    f5Embed,
    lsbEmbed,
    gifShuffleEmbed,
    bsEmbed,
    cptExtract,
    f5Extract,
    lsbExtract,
    gifShuffleExtract,
    bsExtract,
)

# pylint: disable=too-many-branches,too-many-statements
def algo(request, algo_name):
    text = ""
    atype = ""
    algo_object = get_object_or_404(Algo, shortTitle=algo_name)
    manual = get_object_or_404(ManPage, algo=algo_object)

    embedFormDict = {
        "cpt": CPTEmbedForm,
        "f5": F5EmbedForm,
        "lsb": LsbEmbedForm,
        "gifshuffle": GifShuffleEmbedForm,
        "bs": BattlestegEmbedForm,
    }

    extractFormDict = {
        "cpt": CPTExtractForm,
        "f5": F5ExtractForm,
        "lsb": LsbExtractForm,
        "gifshuffle": GifShuffleExtractForm,
        "bs": BattlestegExtractForm,
    }
    typeDict = {
        "cpt": "png",
        "f5": "jpeg",
        "lsb": "png",
        "gifshuffle": "gif",
        "bs": "png",
    }

    if request.method == "POST":

        q = Queue()
        # embedding
        if "submit1" in request.POST:

            algoDict = {
                "cpt": cptEmbed,
                "f5": f5Embed,
                "lsb": lsbEmbed,
                "gifshuffle": gifShuffleEmbed,
                "bs": bsEmbed,
            }

            embedForm = embedFormDict[algo_name](request.POST, request.FILES)
            extractForm = extractFormDict[algo_name]()
            atype = typeDict[algo_name]
            p = Process(target=algoDict[algo_name], args=(q,))

            # fork process to embed
            if embedForm.is_valid():
                p.start()
                q.put([request.POST, request.FILES["file"].temporary_file_path()])
                os.system("sleep 1")
                try:
                    retval = q.get(True, 10)
                except Q.Empty:
                    retval = -2
                p.join()
                if retval == -1:
                    text += "%s-Datei nicht gefunden oder fehlerhaft." % (atype)
                elif retval == -2:
                    text += "Fehler beim Einbetten. Anderes Bild oder andere Parameter versuchen."
                else:
                    return createResponse(retval, atype)
        # extracting
        elif "submit2" in request.POST:

            algoDict = {
                "cpt": cptExtract,
                "f5": f5Extract,
                "lsb": lsbExtract,
                "gifshuffle": gifShuffleExtract,
                "bs": bsExtract,
            }

            embedForm = embedFormDict[algo_name]()
            extractForm = extractFormDict[algo_name](request.POST, request.FILES)
            atype = typeDict[algo_name]
            p = Process(target=algoDict[algo_name], args=(q,))

            # fork process to extract
            if extractForm.is_valid():
                p.start()
                q.put([request.POST, request.FILES["file"].temporary_file_path()])
                try:
                    retval = q.get(True, 10)
                except Q.Empty:
                    retval = -2
                p.join()
                if retval == -1:
                    text += "%s-Datei nicht gefunden oder fehlerhaft." % (atype)
                elif retval == -2:
                    text += "Fehler beim Ausbetten. Anderes Bild oder andere Parameter versuchen."
                else:
                    # print retval
                    text += retval
    # empty form
    else:
        embedForm = embedFormDict[algo_name]()
        extractForm = extractFormDict[algo_name]()
    # render
    return render_to_response(
        "stego_algo.html",
        {
            "algo": algo_object,
            "embedForm": embedForm,
            "extractForm": extractForm,
            "text": text,
            "algo_type": "Staganographie",
            "manual": manual,
        },
    )
# pylint: enable=too-many-branches,too-many-statements


def createResponse(filename, ftype):
    with open(filename) as file_handle:
        wrapper = FileWrapper(file_handle)

    response = HttpResponse(wrapper, mimetype="image/%s" % (ftype))
    response["Content-Length"] = os.path.getsize(filename)

    response["Content-Disposition"] = "attachment; filename=stego.%s" % (ftype)
    return response
