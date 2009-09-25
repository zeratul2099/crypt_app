from crypt_app.stego.models import CPTEmbedForm, CPTExtractForm
from crypt_app.base_app.models import Algo, InfoPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader


def algo(request, algo):
    algo_object = get_object_or_404(Algo, shortTitle=algo)
    if request.method == 'POST':
        embedForm = CPTEmbedForm(request.POST, request.FILES)
    else:
        
        embedForm = CPTEmbedForm()
        extractForm = CPTExtractForm()
    return render_to_response("stego_algo.html", {'title' : algo_object.name,
                                            'algo' : algo,
                                            'embedForm' : embedForm, 
                                            'extractForm' : extractForm,}) 
