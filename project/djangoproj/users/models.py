from django.db import models

class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    def __unicode__(self):
        return u'%s\t%s' % (self.username, self.password)
