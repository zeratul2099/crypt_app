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


from django.db import models

class Algo(models.Model):
    name = models.CharField(max_length=30, unique=True)
    shortTitle = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=10)
    order = models.IntegerField()
    def __unicode__(self):
        return self.name

class InfoPage(models.Model):

    algo = models.ForeignKey(Algo)
    text = models.TextField()
    image = models.CharField(max_length=20)
    i_caption = models.CharField(max_length=100, blank=True, null=True)
    i_width = models.IntegerField(blank=True, null=True)
    i_height = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=50)
    shortTitle = models.CharField(max_length=10)
    masterPage = models.ForeignKey('self', blank=True, null=True)
    order = models.IntegerField()
    def __unicode__(self):
        return self.algo.name+": "+self.title

class ManPage(models.Model):

    algo = models.ForeignKey(Algo, unique=True)
    text = models.TextField()
    def __unicode__(self):
        return self.algo.name
