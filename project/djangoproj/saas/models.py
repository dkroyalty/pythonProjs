from django.db import models

class TaxStandard(models.Model):
    taxbyself = models.IntegerField(default=0)
    taxbyother = models.IntegerField(default=0)
    taxrate = models.IntegerField(default=0, db_index=True)
    taxfastsub = models.IntegerField(default=0)

    class Meta:
        ordering = ['taxrate']

    def __unicode__(self):
        return u'%d\t%d\t%d' % (self.taxbyself, self.taxbyother, self.taxrate)
