from crypt_app.hash.models import HashForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader
from KeccakHash import KeccakHash
from datetime import datetime
import hashlib, random, sys


def hash(request):
    return render_to_response("hash.html")

def algo_keccak(request):
    salt = 0
    salt_str = ''
    if request.method == 'POST':
        
        if request.FILES:
            if request.FILES['file'].size > 10000:
                form = HashForm()
                return render_to_response("hash_algo.html", {'hashvalue' : 'Datei zu gross',  'form' : form}) 
            clear_text = request.FILES['file'].read()
            output = "Eingabedatei:\n%s (%s Bytes)\n" %(request.FILES['file'].name,
                                                      request.FILES['file'].size)
        else:
            clear_text = request.POST.get("clear", "")
            output = "Eingabestring:\n%s\n" %(clear_text)
            
        if 'withSalt' in request.POST:
            rand = random.Random(datetime.now().strftime('%s'))
            salt = rand.randint(0, sys.maxint)
            for i in range(4):
                salt_str += chr((salt%(1<<(8*(i+1))))>>((i*8)+1))
            clear_text += salt_str
            
        form = HashForm(request.POST, request.FILES)   
        output += "Keccak[800]-224-Hash:\n"
        output += KeccakHash(repr(clear_text)).hexdigest()
        
        if 'withSalt' in request.POST:
            output += "\nSalt:\n"
            output += repr(salt_str)
    else:
        clear_text = ""
        output = ''
        form = HashForm()
    return render_to_response("hash_algo.html", {'title' : 'Keccak',
                                            'algo' : 'keccak',
                                            'hashvalue' : output,
                                            'clear_text' : clear_text,
                                            'form' : form,}) 


def info_keccak(request, step):
    title = ''
    text = ''
    svg = ''

    if step == 'absorb':
        title = 'Absorb'
        svg = 'absorb.svg'
    elif step == 'squeeze':
        title = 'Squeeze'
        svg = 'squeeze.svg'
    elif step == 'chi':
        title = 'Chi'
        svg = 'chi.svg'
    elif step == 'theta':
        title = 'Theta'
        svg = 'theta.svg'
    elif step == 'pi':
        title = 'Pi'
        svg = 'pi.svg'
    elif step == 'rho':
        title = 'Rho'
        svg = 'rho.svg'
    elif step == 'iota':
        title = 'Iota'
        svg = 'iota.svg'
    else:
        title = 'Keccak'
        text = "Beim Keccak-Algorithmus handelt es sich um einen "
        text += "einen Hash-Algorithmus und SHA-3-Kandidaten. Der"
        text += " Algorithmus verwendet drei grundlegende Funktionen:<br>"
        text += "Die <a href='/hash/info/keccak/absorb/'>Absorb</a>-Funktion, die Squeeze-Funktion sowie die "
        text += "eigentliche Permutations-Funktion, welche nocheinmal "
        text += "in f&uuml;nf Unterfunktionen aufgeteilt ist.<br>Die "
        text += "<a href='/hash/info/keccak/absorb/'>Absorb</a>-Funktion schreibt blockweise die Nachricht "
        text += "in einen State und wendet dazwischen immer wieder "
        text += "die Permutationsfunktion an.<br>Die <a href='/hash/info/keccak/squeeze/'>Squeeze</a>-Funktion "
        text += "schreibt blockweise den State in die Ausgabe und "
        text += "wendet dazwischen ebenso die Permutationsfunktion an."
        text += "<br>Die Permutationsfunktion wendet nacheinander die "
        text += "Funktionen <a href='/hash/info/keccak/chi/'>Chi</a>, "
        text += "<a href='/hash/info/keccak/theta/'>Theta</a>, "
        text += "<a href='/hash/info/keccak/pi/'>Pi</a>, "
        text += "<a href='/hash/info/keccak/rho/'>Rho</a> und "
        text += "<a href='/hash/info/keccak/iota/'>Iota</a> an und "
        text += "wiederholt dies mehrere Runden.<br>Der State ist ein "
        text += "Wert aus 5 x 5 x w Bits, wobei w die l&auml;nge eines "
        text += "CPU-Wortes ist. Zur Visualisierung der Permutationen "
        text += "wird der State in einer dreidimensionalen Blockform "
        text += "dargestellt."
        svg = 'state.svg'
        
    keccak_nav = "<a href='/hash/info/keccak/'>Keccak &Uuml;bersicht</a> | "
    keccak_nav += "<a href='/hash/info/keccak/absorb/'>Absorb</a> | "
    keccak_nav += "<a href='/hash/info/keccak/squeeze/'>Squeeze</a> | "
    keccak_nav += "<a href='/hash/info/keccak/chi/'>Chi</a> | "
    keccak_nav += "<a href='/hash/info/keccak/theta/'>Theta</a> | "
    keccak_nav += "<a href='/hash/info/keccak/pi/'>Pi</a> | "
    keccak_nav += "<a href='/hash/info/keccak/rho/'>Rho</a> | "
    keccak_nav += "<a href='/hash/info/keccak/iota/'>Iota</a>"
    return render_to_response("hash_info.html", {'title' : title,
                                                'text' : text,
                                                'svg' : svg,
                                                'nav' : keccak_nav,
                                                'algo' : 'keccak',
                                                })
