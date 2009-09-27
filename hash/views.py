from crypt_app.hash.models import HashForm
from crypt_app.base_app.models import Algo, InfoPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader
from KeccakHash import KeccakHash
from datetime import datetime
import hashlib, random, sys


def hash(request):
    algos = Algo.objects.filter(type='hash')
        
    return render_to_response("hash.html", { "algos" : algos })


def algo(request, algo):
    salt = 0
    salt_str = ''
    algo_object = get_object_or_404(Algo, shortTitle=algo)
    if request.method == 'POST':
        
        if request.FILES:
            if request.FILES['file'].size > 10000 and algo=="keccak":
                form = HashForm()
                return render_to_response("hash_algo.html", {'hashvalue' : 'Datei zu gross',  'form' : form}) 
            clear_text = request.FILES['file'].read()
            output = "Eingabedatei:\n%s (%s Bytes)\n" %(request.FILES['file'].name,
                                                      request.FILES['file'].size)
        else:
            clear_text = request.POST.get("clear", "")
            output = "Eingabestring:\n%s\n\n" %(clear_text)
            
        if 'withSalt' in request.POST:
            rand = random.Random(datetime.now().strftime('%s'))
            salt = rand.randint(0, sys.maxint)
            for i in range(4):
                salt_str += chr((salt%(1<<(8*(i+1))))>>((i*8)+1))
            clear_text += salt_str
            
        form = HashForm(request.POST, request.FILES)
        if algo == "keccak":   
            output += "Keccak[800]-224-Hash:\n"
            output += KeccakHash(repr(clear_text)).hexdigest()
        elif algo == "md5":
            output += "MD5-Hash:\n"
            output += hashlib.md5(clear_text).hexdigest() 
        elif algo == "sha1":
            output += "SHA-1-Hash:\n"
            output += hashlib.sha1(clear_text).hexdigest()        
        elif algo == "sha2":
            output += "SHA-2-224-Hash:\n"
            output += hashlib.sha224(clear_text).hexdigest()   
            output += "\n\nSHA-2-256-Hash:\n"
            output += hashlib.sha256(clear_text).hexdigest()   
            output += "\n\nSHA-2-384-Hash:\n"
            output += hashlib.sha384(clear_text).hexdigest()   
            output += "\n\nSHA-2-512-Hash:\n"
            output += hashlib.sha512(clear_text).hexdigest()   
        else:
            output += "Invalid algorithm"
        if 'withSalt' in request.POST:
            output += "\n\nSalt:\n"
            output += repr(salt_str)
    else:
        clear_text = ""
        output = ''
        form = HashForm()
    return render_to_response("hash_algo.html", {'title' : algo_object.name,
                                            'algo' : algo,
                                            'hashvalue' : output,
                                            'clear_text' : clear_text,
                                            'form' : form,}) 



#~ def info(request, algo, page):
    #~ title = ''
    #~ text = ''
    #~ svg = ''
    #~ user_agent = request.META['HTTP_USER_AGENT']
    #~ if user_agent.find('WebKit') != -1 or user_agent.find('Presto') != -1 or user_agent.find('Gecko') != -1:
        #~ pictype = "svg"
    #~ else:
        #~ pictype = "gif"
    #~ algo_object = get_object_or_404(Algo, shortTitle=algo)
    #~ info_page = get_object_or_404(InfoPage, algo=algo_object, shortTitle=page)
    #~ svg = info_page.image+"."+pictype
    #~ 
    #~ main_page = get_object_or_404(InfoPage, masterPage=None, algo=algo_object)
    #~ 
    #~ nav = "<ul>"
    #~ nav +="<li><a href='/"+algo_object.type+"/info/"+algo_object.shortTitle+"/"
    #~ nav += main_page.shortTitle+"/'>"+main_page.title+"</a></li><ul>"
    #~ for p in InfoPage.objects.filter(algo=algo_object, masterPage=main_page):
        #~ nav += "<li><a href='/"+algo_object.type+"/info/"+algo_object.shortTitle+"/"
        #~ nav += p.shortTitle+"/'>"+p.title+"</a></li><ul>"
        #~ for q in InfoPage.objects.filter(algo=algo_object, masterPage=p):
            #~ nav += "<li><a href='/"+algo_object.type+"/info/"+algo_object.shortTitle+"/"
            #~ nav += q.shortTitle+"/'>"+q.title+"</a></li>"
        #~ nav += "</ul>"
    #~ nav += "</ul></ul>"
    #~ nav_list = [];
    #~ # doesn't work because of urls inside list :(
    #~ #for p in InfoPage.objects.filter(algo=algo_object, masterPage=main_page):
    #~ #   nav_list.append("<a href='/"+algo_object.type+"/info/"+algo_object.shortTitle+"/"+p.shortTitle+"/'>"+p.title+"</a>")
    #~ return render_to_response("hash_info.html", {'title' : info_page.title,
                                                #~ 'text' : info_page.text,
                                                #~ 'svg' : svg,
                                                #~ 'width' : info_page.i_width,
                                                #~ 'height' : info_page.i_height,
                                                #~ 'caption' : info_page.i_caption,
                                                #~ 'nav' : nav,
                                                #~ 'algo' : algo_object.shortTitle,
                                                #~ 'name' : algo_object.name,
                                                #~ 'user_agent' : user_agent,
                                                #~ })
    
