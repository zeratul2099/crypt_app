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


from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from .models import Algo, InfoPage


def wrongUrl(_request):
    return HttpResponseRedirect("/kryptos/")


def base(_request):
    algos = {}
    algos["crypto"] = Algo.objects.filter(type="crypto").order_by("order")
    algos["stego"] = Algo.objects.filter(type="stego").order_by("order")
    algos["hash"] = Algo.objects.filter(type="hash").order_by("order")
    return render_to_response("base_app.html", algos)

def about(_request):
    return render_to_response("about.html")

def list(_request, algo_type): # pylint: disable=redefined-builtin
    algos = Algo.objects.filter(type=algo_type).order_by("order")
    if algo_type == "hash":
        title = "Hash-Algorithmen"
    elif algo_type == "stego":
        title = "Steganographie"
    elif algo_type == "crypto":
        title = "Kryptographie"
    else:
        title = ""

    return render_to_response("list.html", {
        "algos": algos,
        "title": title,
        "algo_type": algo_type
    })

def info(request, algo_name, page):
    user_agent = request.META['HTTP_USER_AGENT']
    pictype = "svg"
    algo_object = get_object_or_404(Algo, shortTitle=algo_name)
    info_page = get_list_or_404(InfoPage, algo=algo_object, shortTitle=page)[0]
    main_page = get_list_or_404(InfoPage, masterPage=None, algo=algo_object)[0]

    # generating menu list
    nav_list = []
    if page == "overview":
        nav_list.append("<li id='active' >"+main_page.title+"</li>")
    else:
        nav_list.append("<li><a href='../"+main_page.shortTitle+"/'>"+main_page.title+"</a></li>")
    nav_list.append([])
    for p_page in InfoPage.objects.filter(
            algo=algo_object,
            masterPage=main_page
    ).order_by("order"):
        if p_page.shortTitle == page:
            nav_list[1].append("<li id='active'>"+p_page.title+"</li>")
        else:
            nav_list[1].append("<li><a href='../"+p_page.shortTitle+"/'>"+p_page.title+"</a></li>")
        sublist = []
        for q_page in InfoPage.objects.filter(
                algo=algo_object,
                masterPage=p_page
        ).order_by("order"):
            if q_page.shortTitle == page:
                sublist.append("<li id='active'>"+q_page.title+"</li>")
            else:
                sublist.append(
                    "<li><a href='../../" +\
                    algo_object.shortTitle +\
                    "/" +\
                    q_page.shortTitle +\
                    "/'>" +\
                    q_page.title +\
                    "</a></li>"
                )
        if sublist:
            nav_list[1].append(sublist)
    type_long = ""
    if algo_object.type == 'crypto':
        type_long = "Kryptographie"
    elif algo_object.type == 'stego':
        type_long = "Steganographie"
    elif algo_object.type == 'hash':
        type_long = "Hash-Algorithmen"
    return render_to_response("infopage.html", {
        'infopage': info_page,
        'pictype': pictype,
        'navlist': nav_list,
        'algo_type': type_long,
        'user_agent': user_agent,
    })
