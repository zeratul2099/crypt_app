from crypt_app.base_app.models import Algo, InfoPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader


def base(request):
    return render_to_response("base_app.html")

def list(request, algo_type):
    algos = Algo.objects.filter(type=algo_type)
        
    return render_to_response("list.html", { "algos" : algos })
