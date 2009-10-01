from crypt_app.stego.models import CPTEmbedForm, CPTExtractForm
from crypt_app.stego.models import F5EmbedForm, F5ExtractForm
from crypt_app.stego.models import LsbEmbedForm, LsbExtractForm
from crypt_app.stego.models import GifShuffleEmbedForm, GifShuffleExtractForm
from crypt_app.stego.models import BattlestegEmbedForm, BattlestegExtractForm
from crypt_app.base_app.models import Algo, InfoPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader
from django.core.servers.basehttp import FileWrapper
from processing import Process, Pipe, Queue
import Queue as Q
import libstego, libstegofile, os

def algo(request, algo):
    text = ""
    type = ""
    algo_object = get_object_or_404(Algo, shortTitle=algo)
    if request.method == 'POST':
        q = Queue()
        # embedding
        if "submit1" in request.POST:

            if algo == "cpt":
                embedForm = CPTEmbedForm(request.POST, request.FILES)
                extractForm = CPTExtractForm()
                type = "png"
                p = Process(target=cptEmbed, args=(q, ))
                    
            elif algo == "f5":
                embedForm = F5EmbedForm(request.POST, request.FILES)
                extractForm = F5ExtractForm()
                type = "jpeg"
                p = Process(target=f5Embed, args=(q, ))
                    
            elif algo == "lsb":
                embedForm = LsbEmbedForm(request.POST, request.FILES)
                extractForm = LsbExtractForm()
                type = "png"
                p = Process(target=lsbEmbed, args=(q, ))
                    
            elif algo == "gifshuffle":
                embedForm = GifShuffleEmbedForm(request.POST, request.FILES)
                extractForm = GifShuffleExtractForm()
                type = "gif"
                p = Process(target=gifShuffleEmbed, args=(q, ))
                    
            elif algo == "bs":
                embedForm = BattlestegEmbedForm(request.POST, request.FILES)
                extractForm = BattlestegExtractForm()
                type = "png"
                p = Process(target=bsEmbed, args=(q, ))
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
                    text += "No %s file or %s file could not be read."%(type, type)
                elif retval == -2:
                    text += "Error on embedding. Try another image or different parameter."
                else:
                    return createResponse(retval, type)
        # extracting        
        elif "submit2" in request.POST:
    
            if algo == "cpt":
                embedForm = CPTEmbedForm()
                extractForm = CPTExtractForm(request.POST, request.FILES)
                type = "png"
                p = Process(target=cptExtract, args=(q, ))
                    
            elif algo == "f5":
                embedForm = F5EmbedForm()
                extractForm = F5ExtractForm(request.POST, request.FILES)
                type = "jpeg"
                p = Process(target=f5Extract, args=(q, ))

            elif algo == "lsb":
                embedForm = LsbEmbedForm()
                extractForm = LsbExtractForm(request.POST, request.FILES)
                type = "png"
                p = Process(target=lsbExtract, args=(q, ))

            elif algo == "gifshuffle":
                print "gifshuffle extracting..."
                embedForm = GifShuffleEmbedForm()
                extractForm = GifShuffleExtractForm(request.POST, request.FILES)
                type = "gif"
                p = Process(target=gifShuffleExtract, args=(q, ))

            elif algo == "bs":
                embedForm = BattlestegEmbedForm()
                extractForm = BattlestegExtractForm(request.POST, request.FILES)
                type = "png"
                p = Process(target=bsExtract, args=(q, ))
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
                    text += "\nNo %s file or %s file could not be read."%(type, type)
                elif retval == -2:
                    text += "Error on extracting. Try another image or different parameter."
                else:
                    text += retval
    # empty form
    else:
        if algo == "cpt":
            embedForm = CPTEmbedForm()
            extractForm = CPTExtractForm()
        elif algo == "f5":
            embedForm = F5EmbedForm()
            extractForm = F5ExtractForm()
        elif algo == "lsb":
            embedForm = LsbEmbedForm()
            extractForm = LsbExtractForm()
        elif algo == "gifshuffle":
            embedForm = GifShuffleEmbedForm()
            extractForm = GifShuffleExtractForm()
        elif algo == "bs":
            embedForm = BattlestegEmbedForm()
            extractForm = BattlestegExtractForm()
    # render
    return render_to_response("stego_algo.html", {'title' : algo_object.name,
                                            'algo' : algo,
                                            'embedForm' : embedForm, 
                                            'extractForm' : extractForm,
                                            'text' : text}) 

def createResponse(filename, type):
    wrapper = FileWrapper(file(filename))

    response = HttpResponse(wrapper, mimetype='image/%s'%(type))
    response['Content-Length'] = os.path.getsize(filename)

    response['Content-Disposition'] = 'attachment; filename=stego.%s'%(type)
    return response

    

def cptEmbed(q):
    print "Child process"
    post, filename = q.get()
    rgb_data = libstegofile.rgb_data_t()
    stego_data = libstegofile.rgb_data_t()
    png_struct = libstegofile.png_internal_data_t()
    print "received request, opening file..."
    retcode = libstegofile.io_png_read(filename,rgb_data, png_struct)
    if retcode == 0:
        pass
    else:
        print "File open failed"
        q.put(-1)
        return -1
    para = libstegofile.cpt_parameter()
    message = str(post['message'])
    para.password = str(post['pw'])
    para.pwlen = len(para.password)
    para.block_width = int(post['width'])
    para.block_height = int(post['height'])
    print "file opened, embedding..."
    retcode = libstego.cpt_embed(rgb_data, stego_data, message, len(message), para)
    print "integrating..."
    libstegofile.io_png_integrate(png_struct, stego_data)
    print "writing..."
    libstegofile.io_png_write(filename, png_struct)
    q.put(filename)
    print "Child process finished"
                    




def cptExtract(q):
    post, filename = q.get()
    rgb_data = libstegofile.rgb_data_t()
    png_struct = libstegofile.png_internal_data_t()
    retcode = libstegofile.io_png_read(filename, rgb_data, png_struct)
    if retcode == 0:
        pass
    else:
        return -1
    para = libstegofile.cpt_parameter()
    para.password = str(post['pw'])
    para.pwlen = len(para.password)
    para.block_width = int((post['width']))
    para.block_height = int((post['height']))
    stegomsg = libstego.new_charp()
    stegolen = libstego.new_intp()
    libstego.cpt_extract(rgb_data, stegomsg, stegolen, para)
    q.put(str(libstego.charp_value(stegomsg)))

def f5Embed(q):
    post, filename = q.get()
    jpeg_data = libstegofile.jpeg_data_t()
    stego_data = libstegofile.jpeg_data_t()
    jpeg_struct = libstegofile.jpeg_internal_data_t()
    retcode = libstegofile.io_jpeg_read(filename,jpeg_data, jpeg_struct)
    if retcode == 0:
        pass
    else:
        return -1
    para = libstegofile.f5_parameter()
    message = str(post['message'])
    para.password = str(post['pw'])
    para.pwlen = len(para.password)
    libstego.f5_embed(jpeg_data, stego_data, message, len(message), para)
    libstegofile.io_jpeg_integrate(jpeg_struct, stego_data)
    libstegofile.io_jpeg_write(filename, jpeg_struct)                              
    q.put(filename)

def f5Extract(q):
    post, filename = q.get()
    jpeg_data = libstegofile.jpeg_data_t()
    jpeg_struct = libstegofile.jpeg_internal_data_t()
    para = libstegofile.f5_parameter()
    para.password = str(post['pw'])
    para.pwlen = len(para.password)
    stegomsg = libstego.new_charp()
    stegolen = libstego.new_intp0()
    retcode = libstegofile.io_jpeg_read(filename, jpeg_data, jpeg_struct)
    if retcode == 0:
        pass
    else:
        return -1
    libstego.f5_extract(jpeg_data, stegomsg, stegolen, para)
    q.put(str(libstego.charp_value(stegomsg)))

def lsbEmbed(q):
    post, filename = q.get()
    rgb_data = libstegofile.rgb_data_t()
    stego_data = libstegofile.rgb_data_t()
    png_struct = libstegofile.png_internal_data_t()
    retcode = libstegofile.io_png_read(filename, rgb_data, png_struct)
    if retcode == 0:
        pass
    else:
        return -1
    para = libstegofile.lsb_parameter_t()
    message = str(post['message'])
    para.password = str(post['pw'])
    para.pwlen = len(para.password)
    para.select_mode = 2
    para.use_msb = 0
    data = libstego.new_charpp()
    datalen = libstego.new_intp()
    libstego.lsb_convert_png(rgb_data, data, datalen)
    libstego.lsb_embed_indirect(libstego.charpp_value(data),
                        libstego.intp_value(datalen), message, len(message), para)
    libstegofile.io_png_integrate(png_struct, rgb_data)
    libstegofile.io_png_write(filename, png_struct)
    q.put(filename)
    
def lsbExtract(q):
    post, filename = q.get()
    rgb_data = libstegofile.rgb_data_t()
    png_struct = libstegofile.png_internal_data_t()
    para = libstegofile.lsb_parameter_t()
    para.password = str(post['pw'])
    para.pwlen = len(para.password)
    para.select_mode = 2
    para.use_msb = 0
    stegomsg = libstego.new_charp()
    stegolen = libstego.new_intp()
    retcode = libstegofile.io_png_read(filename, rgb_data, png_struct)
    if retcode == 0:
        pass
    else:
        return -1
    bytes = libstego.new_charpp()
    num_bytes = libstego.new_intp()
    libstego.lsb_convert_png(rgb_data, bytes, num_bytes)

    libstego.lsb_extract_indirect(libstego.charpp_value(bytes),
                        libstego.intp_value(num_bytes), stegomsg, stegolen, para)
    msglen = libstego.intp_value(stegolen)
    q.put((str(libstego.charp_value(stegomsg)))[0:msglen])

def gifShuffleEmbed(q):
    post, filename = q.get()
    palette_data = libstegofile.palette_data_t()
    stego_data = libstegofile.palette_data_t()
    gif_struct = libstegofile.gif_internal_data_t()
    retcode = libstegofile.io_gif_read(filename, palette_data, gif_struct)
    if retcode == 0:
        pass
    else:
        return -1
    para = libstegofile.gifshuffle_parameter()
    message = str(post['message'])
    para.password = str(post['pw'])
    para.pwlen = len(para.password)
    libstego.gifshuffle_embed(palette_data, stego_data, message, len(message), para)
    libstegofile.io_gif_integrate(gif_struct, stego_data)
    libstegofile.io_gif_write(filename, gif_struct)
    q.put(filename)

def gifShuffleExtract(q):
    print "GifExtract..."
    post, filename = q.get()
    palette_data = libstegofile.palette_data_t()
    gif_struct = libstegofile.gif_internal_data_t()
    para = libstegofile.gifshuffle_parameter()
    para.password = str(post['pw'])
    para.pwlen = len(para.password)
    stegomsg = libstego.new_charp()
    stegolen = libstego.new_intp()
    retcode = libstegofile.io_gif_read(filename, palette_data, gif_struct)
    if retcode == 0:
        pass
        print "Valid gif at extracting"
    else:
        return -1
    print "Extracting..."
    libstego.gifshuffle_extract(palette_data, stegomsg, stegolen, para)
    print "Message: "+ str(libstego.charp_value(stegomsg))
    q.put(str(libstego.charp_value(stegomsg)))

def bsEmbed(q):
    post, filename = q.get()
    rgb_data = libstegofile.rgb_data_t()
    stego_data = libstegofile.rgb_data_t()
    png_struct = libstegofile.png_internal_data_t()
    retcode = libstegofile.io_png_read(filename, rgb_data, png_struct)
    if retcode == 0:
        pass
    else:
        return -1
    para = libstegofile.battlesteg_parameter()
    message = str(post['message'])
    para.password = str(post['pw'])
    para.pwlen = len(para.password)
    para.startbit = int((post['startbit']))
    para.move_away = int((post['move_away']))
    para.range = int((post['range']))
    libstego.battlesteg_embed(rgb_data, stego_data, message, len(message), para)
    libstegofile.io_png_integrate(png_struct, stego_data)
    libstegofile.io_png_write(filename, png_struct)
    q.put(filename)

def bsExtract(q):
    post, filename = q.get()
    rgb_data = libstegofile.rgb_data_t()
    png_struct = libstegofile.png_internal_data_t()
    retcode = libstegofile.io_png_read(filename, rgb_data, png_struct)
    if retcode == 0:
        pass
    else:
        return -1
    para = libstegofile.battlesteg_parameter()
    para.password = str(post['pw'])
    para.pwlen = len(para.password)
    para.startbit = int((post['startbit']))
    para.move_away = int((post['move_away']))
    para.range = int((post['range']))
    stegomsg = libstego.new_charp()
    stegolen = libstego.new_intp()
    libstego.battlesteg_extract(rgb_data, stegomsg, stegolen, para)
    msglen = libstego.intp_value(stegolen)
    q.put((str(libstego.charp_value(stegomsg)))[0:msglen])
