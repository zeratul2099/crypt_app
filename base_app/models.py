from django.db import models



class Algo(models.Model):
    name = models.CharField(max_length=30, unique=True)
    shortTitle = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=10)
    def __unicode__(self):
        return self.name
        
class InfoPage(models.Model):
    
    algo = models.ForeignKey(Algo)
    text = models.TextField()
    image = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    shortTitle = models.CharField(max_length=10)
    masterPage = models.ForeignKey('self', blank=True, null=True)
    def __unicode__(self):
        return self.title
    
        
