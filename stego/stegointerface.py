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

import libstego # pylint: disable=import-error
import libstegofile # pylint: disable=import-error

def cptEmbed(q):
    post, filename = q.get()
    rgb_data = libstegofile.rgb_data_t()
    stego_data = libstegofile.rgb_data_t()
    png_struct = libstegofile.png_internal_data_t()
    retcode = libstegofile.io_png_read(filename, rgb_data, png_struct)
    if retcode == 0:
        pass
    else:
        q.put(-1)
        return -1
    para = libstegofile.cpt_parameter()
    message = str(post['message'])
    para.password = str(post['pw'])
    para.pwlen = len(para.password)
    para.block_width = int(post['width'])
    para.block_height = int(post['height'])
    retcode = libstego.cpt_embed(rgb_data, stego_data, message, len(message), para)
    libstegofile.io_png_integrate(png_struct, stego_data)
    libstegofile.io_png_write(filename, png_struct)
    q.put(filename)





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
    retcode = libstegofile.io_jpeg_read(filename, jpeg_data, jpeg_struct)
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
    stegolen = libstego.new_intp()
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
    libstego.lsb_embed_indirect(
        libstego.charpp_value(data),
        libstego.intp_value(datalen),
        message,
        len(message),
        para
    )
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
    buf = libstego.new_charpp()
    num_bytes = libstego.new_intp()
    libstego.lsb_convert_png(rgb_data, buf, num_bytes)

    libstego.lsb_extract_indirect(
        libstego.charpp_value(buf),
        libstego.intp_value(num_bytes),
        stegomsg,
        stegolen,
        para
    )
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
    else:
        return -1
    libstego.gifshuffle_extract(palette_data, stegomsg, stegolen, para)
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
