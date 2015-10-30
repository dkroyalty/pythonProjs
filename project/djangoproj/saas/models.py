from django.db import models
import datetime

class TaxStandard(models.Model):
    taxbyself = models.IntegerField(default=0)
    taxbyother = models.IntegerField(default=0)
    taxrate = models.IntegerField(default=0, db_index=True)
    taxfastsub = models.IntegerField(default=0)

    class Meta:
        ordering = ['taxrate']

    def __unicode__(self):
        return u'%d\t%d\t%d' % (self.taxbyself, self.taxbyother, self.taxrate)


class TypeMaster(models.Model):
    typename = models.CharField(max_length=255, db_index=True)

    def __unicode__(self):
        return u'%s' % (typename)


class StatusMaster(models.Model):
    status = models.CharField(max_length=255, db_index=True)

    def __unicode__(self):
        return u'%s' % (status)


class ItemData(models.Model):
    itemname = models.CharField(max_length=255, db_index=True)
    itemimg = models.CharField(max_length=255)
    itemtype = models.ForeignKey(TypeMaster, db_index=True)
    itemstatus = models.ForeignKey(StatusMaster, db_index=True)
    itemdesc = models.TextField(default='', max_length=500)

    def __unicode__(self):
        return u'%s\t%d\t%s' % (self.itemname, self.itemtype, self.itemimg)


class PlaceData(models.Model):
    placename = models.CharField(max_length=255, db_index=True)
    placeimg = models.CharField(max_length=255)
    imgrect = models.CharField(max_length=255)
    placedesc = models.TextField(default='', max_length=500)

    def __unicode__(self):
        return u'%s\t%s' % (self.placename, self.placeimg)


class PlaceRelations(models.Model):
    parentplace = models.ForeignKey(PlaceData,
        related_name='parent_id', db_index=True)
    sonplace = models.ForeignKey(PlaceData,
        related_name='son_id', db_index=True)


class PlaceHoldItems(models.Model):
    placedata = models.ForeignKey(PlaceData, db_index=True)
    itemdata = models.ForeignKey(ItemData, db_index=True)
    createdata = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ['createdata']
