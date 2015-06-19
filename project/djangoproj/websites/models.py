from django.db import models

class Websites(models.Model):
    webseq = models.IntegerField(default=0)
    website = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    detail = models.TextField()

    class Meta:
        ordering = ['webseq', 'desc']

    def __unicode__(self):
        return u'%d\t%s\t%s' % (self.webseq, self.desc, self.website)
