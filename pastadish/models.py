from django.db import models

# Create your models here.
class Paste(models.Model):
    key = models.CharField(max_length=40)
    text = models.TextField()

    def __unicode__(self):
        return u'%s' % (self.text)
