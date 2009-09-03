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

def algo_md5(request):
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
        output += "MD5-Hash:\n"
        output += hashlib.md5(clear_text).hexdigest()
        
        if 'withSalt' in request.POST:
            output += "\nSalt:\n"
            output += repr(salt_str)
    else:
        clear_text = ""
        output = ''
        form = HashForm()
    return render_to_response("hash_algo.html", {'title' : 'MD5',
                                            'algo' : 'md5',
                                            'hashvalue' : output,
                                            'clear_text' : clear_text,
                                            'form' : form,}) 

#~ def info_keccak(request, step):
#~ 
    #~ title = ''
    #~ text = ''
    #~ svg = ''
    #~ user_agent = request.META['HTTP_USER_AGENT']
    #~ if user_agent.find('WebKit') != -1 or user_agent.find('Presto') != -1:
        #~ pictype = "svg"
    #~ else:
        #~ pictype = "gif"
    #~ if step == 'absorb':
        #~ title = 'Absorb-Funktion'
        #~ svg = 'absorb.'+pictype
        #~ text = "Die Absorb-Funktion schreibt die Nachricht blockweise in einen "
        #~ text += "State und wendet die Permutationsfunktionen auf diesen "
        #~ text += "an.<p>Je nach Keccak-Variante wird ein initialer State "
        #~ text += "mit 5 * 5 * 32 (Keccak[800]) oder 5 * 5 * 64 (Keccak[1600]) Nullbits erstellt. Nun "
        #~ text += "werden die ersten r Bits der Nachricht mit den ersten "
        #~ text += "r Bits des States XOR-verkn&uuml;pft und die f&uuml;nf Permutationsfunktionen "
        #~ text += "mehrfach auf den State angewendet. Dabei wird immer mit der "
        #~ text += "<a href='/hash/info/keccak/theta/'>Theta</a>-Permutation begonnen. "
        #~ text += "Die Reihenfolge der restlichen Permutationen ist beliebig. "
        #~ text += "Alle Permutationen werden jedoch in 17 Runden bei Keccak[800] "
        #~ text += "bzw. in 18 Runden bei Keccak[1600] wiederholt.<p>"
        #~ text += "Daraufhin werden die n&auml;chsten r Bits der Nachricht "
        #~ text += "mit dem State XOR-verkn&uuml;pft und wieder die Keccak-Permutationen "
        #~ text += "angewendet. Dies wird so lange wiederholt, bis die komplette "
        #~ text += "Nachricht verarbeitet ist. Auf den resultierenden State "
        #~ text += "wird nun die <a href='/hash/info/keccak/squeeze/'>Squeeze</a>-Funktion "
        #~ text += "angewendet, um den Hashwert zu erzeugen."
    #~ elif step == 'squeeze':
        #~ title = 'Squeeze-Funktion'
        #~ svg = 'squeeze.'+pictype
        #~ text = "Die Squeeze-Funktion erzeugt aus dem durch die "
        #~ text += "<a href='/hash/info/keccak/absorb/'>Absorb</a>-Funktion "
        #~ text += "produziertem State einen beliebig langen Hashwert.<p>"
        #~ text += "Hierzu werden die ersten r Bits des States als die "
        #~ text += "ersten r Bits des Hashes verwendet. Dann wird wiederum "
        #~ text += "die Keccak-Permutation angewendet und wieder die ersten "
        #~ text += "r Bits des States ausgelesen und in den Hashwert geschrieben. "
        #~ text += "Dies kann so lange wiederholt werden, bis man einen Hashwert "
        #~ text += "von gew&uuml;nschter L&auml;nge hat. M&ouml;glich ist "
        #~ text += "ist dabei auch ein unendlich langer Hashstrom."
    #~ elif step == 'chi':
        #~ title = 'Chi-Permutation'
        #~ svg = 'chi.'+pictype
        #~ text = "Die Chi-Permutation wird Plane-weise auf den State angewendet, "
        #~ text += "es werden also immer f&uuml;nf 32- oder 64-bit Werte betrachtet.<p>"
        #~ text += "Jede einzelne Lane, also jeder 32- oder 64-bit Wert wird "
        #~ text += "aus sich selbst und den beiden folgenden (rechts davon befindlichen) Lanes berechnet. "
        #~ text += "Befindet sich die Lane am rechten Ende des Planes wird "
        #~ text += "umgebrochen und die ersten Lanes des gleichen Planes als "
        #~ text += "die folgenden betrachtet.<p>"
        #~ text += "Zur Berechnung der neuen Lane wird das Inverse der "
        #~ text += "n&auml;chsten Lane mit der &uuml;bern&auml;chsten "
        #~ text += "AND-verkn&uuml;pft und anschlie&szlig;end mit dem alten Wert "
        #~ text += "von sich selbst XOR-verkn&uuml;pft.<p>"
    #~ elif step == 'theta':
        #~ title = 'Theta-Permutation'
        #~ svg = 'theta.'+pictype
        #~ text = "Die Theta-Permutation wird auf jedes Bit des States "
        #~ text += "einzeln angewendet.<p>"
        #~ text += "Hierzu werden die Columns links des Bits (x-1) und rechts vorne (x+1, z-1) "
        #~ text += "betrachtet. Die einzelnen Bits der Columns alle werden miteinander "
        #~ text += "XOR-verkn&uuml;pft und dann mit dem zu manipulierenden Bit "
        #~ text += "ebenfalls XOR-verkn&uuml;pft.<p>"
        #~ text += "Diese Operation wird mit jedem Bit des States "
        #~ text += "durchgef&uuml;hrt, kann aber bei der Implementierung "
        #~ text += "insofern vereinfacht werden, jeweils die ganze Lane "
        #~ text += "mit einer einzelnen Operation manipuliert."
    #~ elif step == 'pi':
        #~ title = 'Pi-Permutation'
        #~ svg = 'pi.'+pictype
        #~ text = "Die Pi-Permutation vertauscht die Positionen der Lanes "
        #~ text += "innerhalb des States nach einem bestimmten Schema<p>"
        #~ text += "Die neue Position jeder Lane wird nach<p>"
        #~ text += "<img src='/content/pi_formula.png'><p>"
        #~ text += "berechnet, wobei x und y die alte Position und "
        #~ text += "X und Y die neue Position bestimmen."
    #~ elif step == 'rho':
        #~ title = 'Rho-Permutation'
        #~ svg = 'rho.'+pictype
        #~ text = "Die Rho-Permutation f&uuml;hrt eine bestimmte Anzahl "
        #~ text += "von Rechtsshifts auf jede Lane durch. Die Offsets des "
        #~ text += "Shifts sind folgende:<p>"
        #~ text += "<table border='1' cellspacing='0' width='100%'>"
        #~ text += "<tr><td></td><td>x=3</td><td>x=4</td><td>x=0</td><td>x=1</td><td>x=2</td></tr>"
        #~ text += "<tr><td>y=2</td><td>153</td><td>231</td><td>3</td><td>10</td><td>171</td></tr>"
        #~ text += "<tr><td>y=1</td><td>55</td><td>276</td><td>36</td><td>300</td><td>6</td></tr>"
        #~ text += "<tr><td>y=0</td><td>28</td><td>91</td><td>0</td><td>1</td><td>190</td></tr>"
        #~ text += "<tr><td>y=4</td><td>120</td><td>78</td><td>210</td><td>66</td><td>253</td></tr>"
        #~ text += "<tr><td>y=3</td><td>21</td><td>136</td><td>105</td><td>45</td><td>15</td></tr>"
        #~ text += "</table>"
    #~ elif step == 'iota':
        #~ title = 'Iota-Permutation'
        #~ svg = 'lfsr.'+pictype
        #~ text = "Die Iota-Permutation addiert eine Rundenkonstante auf "
        #~ text += "die erste Lane (x=0, y=0). Diese Rundenkonstante &auml;ndert sich "
        #~ text += "von Runde zu Runde und ist die Ausgabe eines "
        #~ text += "linear r&uuml;ckgekoppeltes Schieberegisters (Linear Feedback Shift Register, LFSR).<p>"
        #~ text += "Ein LFSR ist ein Schieberegister der L&auml;nge n mit einer "
        #~ text += "beliebigen Initialbelegung. Vor jedem Rechtsshift werden "
        #~ text += "die Bits an zuvor festgelegten Positionen XOR-verkn&uuml;pft "
        #~ text += "und das Ergebnis links an das Register angef&uuml;gt. "
        #~ text += "Das Bit am rechten Ende des Registers wird aus Ausgabe "
        #~ text += "verwendet.<p> Mithilfe des LFSR werden Rundenkonstanten "
        #~ text += "berechnet und bei jeder Anwendung von Iota die entsprechende "
        #~ text += "Konstante auf die erste Lane addiert.<p>"
    #~ else:
        #~ title = 'Keccak'
        #~ text = "Beim Keccak-Algorithmus handelt es sich um einen "
        #~ text += "Hash-Algorithmus und SHA-3-Kandidaten. Der"
        #~ text += " Algorithmus verwendet drei grundlegende Funktionen:<p>"
        #~ text += "Die <a href='/hash/info/keccak/absorb/'>Absorb</a>-Funktion, "
        #~ text += "die <a href='/hash/info/keccak/squeeze/'>Squeeze</a>-Funktion sowie die "
        #~ text += "eigentliche Permutations-Funktion, welche noch einmal "
        #~ text += "in f&uuml;nf Unterfunktionen aufgeteilt ist.<p>Die "
        #~ text += "<a href='/hash/info/keccak/absorb/'>Absorb</a>-Funktion schreibt blockweise die Nachricht "
        #~ text += "in einen State und wendet dazwischen immer wieder "
        #~ text += "die Permutationsfunktion an.<br>Die <a href='/hash/info/keccak/squeeze/'>Squeeze</a>-Funktion "
        #~ text += "schreibt blockweise den State in die Ausgabe und "
        #~ text += "wendet dazwischen ebenso die Permutationsfunktion an."
        #~ text += "<br>Die Permutationsfunktion wendet nacheinander die "
        #~ text += "Funktionen <a href='/hash/info/keccak/chi/'>Chi</a>, "
        #~ text += "<a href='/hash/info/keccak/theta/'>Theta</a>, "
        #~ text += "<a href='/hash/info/keccak/pi/'>Pi</a>, "
        #~ text += "<a href='/hash/info/keccak/rho/'>Rho</a> und "
        #~ text += "<a href='/hash/info/keccak/iota/'>Iota</a> an und "
        #~ text += "wiederholt dies mehrere Runden.<br>Der State ist ein "
        #~ text += "Wert aus 5 * 5 * w Bits, wobei w die L&auml;nge eines "
        #~ text += "CPU-Wortes ist. Zur Visualisierung der Permutationen "
        #~ text += "wird der State in einer dreidimensionalen Blockform "
        #~ text += "dargestellt.<p>"
        #~ text += "Die genaue Spezifikation des Keccak-Algorithmus ist unter<p>"
        #~ text += "<a href='http://keccak.noekeon.org/'>keccak.noekeon.org</a><p>"
        #~ text += "zu finden."
        #~ svg = 'state.'+pictype
        #~ 
    #~ keccak_nav = "<ul><li><a href='/hash/info/keccak/'>Keccak &Uuml;bersicht</a></li>"
    #~ keccak_nav += "<ul><li><a href='/hash/info/keccak/absorb/'>Absorb</a></li>"
    #~ keccak_nav += "<li><a href='/hash/info/keccak/squeeze/'>Squeeze</a></li>"
    #~ keccak_nav += "<li>Keccak-Permutationen</li>"
    #~ keccak_nav += "<ul><li><a href='/hash/info/keccak/chi/'>Chi</a></li>"
    #~ keccak_nav += "<li><a href='/hash/info/keccak/theta/'>Theta</a></li>"
    #~ keccak_nav += "<li><a href='/hash/info/keccak/pi/'>Pi</a></li>"
    #~ keccak_nav += "<li><a href='/hash/info/keccak/rho/'>Rho</a></li>"
    #~ keccak_nav += "<li><a href='/hash/info/keccak/iota/'>Iota</a></ul></ul></ul>"
    #~ return render_to_response("hash_info.html", {'title' : title,
                                                #~ 'text' : text,
                                                #~ 'svg' : svg,
                                                #~ 'nav' : keccak_nav,
                                                #~ 'algo' : 'keccak',
                                                #~ 'name' : 'Keccak',
                                                #~ 'user_agent' : user_agent,
                                                #~ })




def info(request, algo, page):
    title = ''
    text = ''
    svg = ''
    user_agent = request.META['HTTP_USER_AGENT']
    if user_agent.find('WebKit') != -1 or user_agent.find('Presto') != -1:
        pictype = "svg"
    else:
        pictype = "gif"
    algo_object = get_object_or_404(Algo, shortTitle=algo)
    info_page = get_object_or_404(InfoPage, algo=algo_object, shortTitle=page)
    svg = info_page.image+"."+pictype
    
    main_page = get_object_or_404(InfoPage, masterPage=None, algo=algo_object)
    
    nav = "<ul>"
    nav +="<li><a href='/"+algo_object.type+"/info/"+algo_object.shortTitle+"/"
    nav += main_page.shortTitle+"/'>"+main_page.title+"</a></li><ul>"
    for p in InfoPage.objects.filter(algo=algo_object, masterPage=main_page):
        nav += "<li><a href='/"+algo_object.type+"/info/"+algo_object.shortTitle+"/"
        nav += p.shortTitle+"/'>"+p.title+"</a></li><ul>"
        for q in InfoPage.objects.filter(algo=algo_object, masterPage=p):
            nav += "<li><a href='/"+algo_object.type+"/info/"+algo_object.shortTitle+"/"
            nav += q.shortTitle+"/'>"+q.title+"</a></li>"
        nav += "</ul>"
    nav += "</ul></ul>"
    return render_to_response("hash_info.html", {'title' : info_page.title,
                                                'text' : info_page.text,
                                                'svg' : svg,
                                                'nav' : nav,
                                                'algo' : algo_object.shortTitle,
                                                'name' : algo_object.name,
                                                'user_agent' : user_agent,
                                                })
    
