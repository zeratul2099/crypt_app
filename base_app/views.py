from crypt_app.base_app.models import Algo, InfoPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader


def base(request):
    return render_to_response("base_app.html")

def list(request, algo_type):
    algos = Algo.objects.filter(type=algo_type)
    if algo_type == "hash":
        title = "Hashalgorithmen"
    elif algo_type == "stego":
        title = "Steganographie"
    elif algo_type == "crypto":
        title = "Kryptographie"
    else:
        title = ""
        
    return render_to_response("list.html", { "algos" : algos, "title" : title })

def info(request, algo, page):
    title = ''
    text = ''
    svg = ''
    user_agent = request.META['HTTP_USER_AGENT']
    if (user_agent.find('WebKit') != -1 or user_agent.find('Presto') != -1 or user_agent.find('Gecko') != -1):
        pictype = "svg"
    else:
        pictype = "gif"
    algo_object = get_object_or_404(Algo, shortTitle=algo)
    info_page = get_object_or_404(InfoPage, algo=algo_object, shortTitle=page)
    svg = info_page.image+"."+pictype
    
    main_page = get_object_or_404(InfoPage, masterPage=None, algo=algo_object)
    
    nav = "<ul>"
    nav +="<li><a href='/info/"+algo_object.shortTitle+"/"
    nav += main_page.shortTitle+"/'>"+main_page.title+"</a></li><ul>"
    for p in InfoPage.objects.filter(algo=algo_object, masterPage=main_page):
        nav += "<li><a href='/info/"+algo_object.shortTitle+"/"
        nav += p.shortTitle+"/'>"+p.title+"</a></li><ul>"
        for q in InfoPage.objects.filter(algo=algo_object, masterPage=p):
            nav += "<li><a href='/info/"+algo_object.shortTitle+"/"
            nav += q.shortTitle+"/'>"+q.title+"</a></li>"
        nav += "</ul>"
    nav += "</ul></ul>"
    nav_list = [];
    # doesn't work because of urls inside list :(
    #for p in InfoPage.objects.filter(algo=algo_object, masterPage=main_page):
    #   nav_list.append("<a href='/"+algo_object.type+"/info/"+algo_object.shortTitle+"/"+p.shortTitle+"/'>"+p.title+"</a>")
    type_long = ""
    if algo_object.type == 'crypo':
        type_long = "Krytographie"
    elif algo_object.type == 'stego':
        type_long = "Steganographie"
    elif algo_object.type == 'hash':
        type_long = "Hashalgorithmen"
    return render_to_response("hash_info.html", { 'infopage' : info_page,
                                                'svg' : svg,
                                                'nav' : nav,
                                                'algo' : algo_object,
                                                'algo_type' : type_long,
                                                'user_agent' : user_agent,
                                                })
