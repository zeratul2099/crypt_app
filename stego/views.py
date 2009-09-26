from crypt_app.stego.models import CPTEmbedForm, CPTExtractForm
from crypt_app.base_app.models import Algo, InfoPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader
from django.core.servers.basehttp import FileWrapper
import libstego, libstegofile, os

def algo(request, algo):
    text = ""
    algo_object = get_object_or_404(Algo, shortTitle=algo)
    if request.method == 'POST':
        if "submit1" in request.POST:
            embedForm = CPTEmbedForm(request.POST, request.FILES)
            extractForm = CPTExtractForm()
            if embedForm.is_valid():
                if algo == "cpt":
                    #text += request.FILES['file'].url
                    # do libstego work
                    retval = cptEmbed(request)
                    if retval == -1:
                        text += "\nNo PNG File or PNG file could not be read."
                        return render_to_response("stego_algo.html", {'title' : algo_object.name,
                                                'algo' : algo,
                                                'embedForm' : embedForm, 
                                                'extractForm' : extractForm,
                                                'text' : text})
                    else:
                        return retval
            
        elif "submit2" in request.POST:
            embedForm = CPTEmbedForm()
            extractForm = CPTExtractForm(request.POST, request.FILES)
            if extractForm.is_valid():
                if algo == "cpt":
                    retval = cptExtract(request)
                    if retval == -1:
                        text += "\nNo PNG File or PNG file could not be read."
                        return render_to_response("stego_algo.html", {'title' : algo_object.name,
                                                'algo' : algo,
                                                'embedForm' : embedForm, 
                                                'extractForm' : extractForm,
                                                'text' : text})
                    else:
                        text += retval
    else:
        
        embedForm = CPTEmbedForm()
        extractForm = CPTExtractForm()
    return render_to_response("stego_algo.html", {'title' : algo_object.name,
                                            'algo' : algo,
                                            'embedForm' : embedForm, 
                                            'extractForm' : extractForm,
                                            'text' : text}) 


def cptEmbed(request):
    rgb_data = libstegofile.rgb_data_t()
    stego_data = libstegofile.rgb_data_t()
    png_struct = libstegofile.png_internal_data_t()
    retcode = libstegofile.io_png_read(request.FILES['file'].temporary_file_path(),rgb_data, png_struct)
    if retcode == 0 and request.FILES['file'].content_type == "image/png":
        pass
    else:
        return -1
    para = libstegofile.cpt_parameter()
    message = str(request.POST['message'])
    #para.password = request.POST['pw']
    para.password = str(request.POST['pw'])
    para.pwlen = len(para.password)
    para.block_width = int((request.POST['width']))
    para.block_height = int((request.POST['height']))
    retcode = libstego.cpt_embed(rgb_data, stego_data, message, len(message), para)
    libstegofile.io_png_integrate(png_struct, stego_data)
    libstegofile.io_png_write(request.FILES['file'].temporary_file_path(), png_struct)
    
    filename = request.FILES['file'].temporary_file_path() # Select your file here.                                
    wrapper = FileWrapper(file(filename))
    #response = HttpResponse(wrapper, content_type='text/plain')
    response = HttpResponse(wrapper, mimetype='image/png')
    response['Content-Length'] = os.path.getsize(filename)

    response['Content-Disposition'] = 'attachment; filename=stego.png'
    return response

def cptExtract(request):
    rgb_data = libstegofile.rgb_data_t()
    png_struct = libstegofile.png_internal_data_t()
    retcode = libstegofile.io_png_read(request.FILES['file'].temporary_file_path(),rgb_data, png_struct)
    if retcode == 0 and request.FILES['file'].content_type == "image/png":
        pass
    else:
        return -1
    para = libstegofile.cpt_parameter()
    para.password = str(request.POST['pw'])
    para.pwlen = len(para.password)
    para.block_width = int((request.POST['width']))
    para.block_height = int((request.POST['height']))
    stegomsg = libstego.new_charp()
    stegolen = libstego.new_intp()
    libstegofile.io_png_read(request.FILES['file'].temporary_file_path(),rgb_data, png_struct)
    libstego.cpt_extract(rgb_data, stegomsg, stegolen, para)
    return str(libstego.charp_value(stegomsg))
