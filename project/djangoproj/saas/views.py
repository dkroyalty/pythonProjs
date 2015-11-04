from saas.models import *
from django.db.models.loading import get_model

def getOrderedTaxStandard():
    try:
        taxstdlist = TaxStandard.objects.all()
    except TaxStandard.DoesNotExist:
        return None
    return taxstdlist

def getSuitableStandard(untaxincome, calcself=True):
    taxstandard = None
    try:
        taxstdlist = getOrderedTaxStandard()
        for eachstd in taxstdlist:
            if untaxincome <= eachstd.taxbyself and calcself is True:
                taxstandard = eachstd
                break
            elif untaxincome <= eachstd.taxbyother and calcself is False:
                taxstandard = eachstd
                break
            elif eachstd.taxbyself == 0 or eachstd.taxbyother == 0:
                taxstandard = eachstd
                break
    except TaxStandard.DoesNotExist:
        return None
    return taxstandard

def saveNewTaxStandard(taxbyself, taxbyother, taxrate, taxfastsub):
    newstandard = TaxStandard(
            taxbyself = taxbyself,
            taxbyother = taxbyother,
            taxrate = taxrate,
            taxfastsub = taxfastsub,
        )
    newstandard.save()
    return newstandard

def clearDataRecord():
    record = TaxStandard.objects.all.delete()
    return (len(getOrderedWebList()) == 0)

def initDataRecord():
    taxstdlist = getOrderedTaxStandard()
    if taxstdlist is None or len(taxstdlist) == 0:
        saveNewTaxStandard(1500, 1455, 3, 0)
        saveNewTaxStandard(4500, 4155, 10, 105)
        saveNewTaxStandard(9000, 7755, 20, 555)
        saveNewTaxStandard(35000, 27255, 25, 1005)
        saveNewTaxStandard(55000, 41255, 30, 2755)
        saveNewTaxStandard(80000, 57505, 35, 5505)
        saveNewTaxStandard(0, 0, 45, 13505)

def setItemType(typename):
    try:
        typeobj = TypeMaster.objects.get(typename=typename)
        return typeobj
    except TypeMaster.DoesNotExist:
        newtypemst = TypeMaster(
                typename = typename,
            )
        newtypemst.save()
        return newtypemst

def getItemType(typename=None):
    if typename is None:
        try:
            alltype = TypeMaster.objects.all()
            return alltype
        except TypeMaster.DoesNotExist:
            return None
    try:
        typeobj = TypeMaster.objects.get(typename=typename)
        return typeobj
    except TypeMaster.DoesNotExist:
        return None

def setItemStatus(statusname):
    try:
        statusobj = StatusMaster.objects.get(status=statusname)
        return statusobj
    except StatusMaster.DoesNotExist:
        newstatusmst = StatusMaster(
                status = statusname,
            )
        newstatusmst.save()
        return newstatusmst

def getItemStatus(statusname=None):
    if statusname is None:
        try:
            alltype = StatusMaster.objects.all()
            return alltype
        except StatusMaster.DoesNotExist:
            return None
    try:
        statusobj = StatusMaster.objects.get(status=statusname)
        return statusobj
    except StatusMaster.DoesNotExist:
        return None

def setPlaceData(placeid, placename, placeimg, imgrect, desc=''):
    if placeid is None:
        newplacedata = PlaceData(
                placename = placename,
                placeimg = placeimg,
                imgrect = imgrect,
                placedesc = desc,
            )
        newplacedata.save()
        return newplacedata
    try:
        placeobj = PlaceData.objects.filter(id=placeid)
        placeobj.update(
                placename=placename,
                placeimg=placeimg,
                imgrect=imgrect,
                placedesc=desc,
            )
        return placeobj
    except PlaceData.DoesNotExist:
        return None

def getPlaceData(placeid=None):
    if placeid is None:
        try:
            allplace = PlaceData.objects.all()
            return allplace
        except PlaceData.DoesNotExist:
            return None
    else:
        try:
            specifyplace = PlaceData.objects.get(id=placeid)
            return specifyplace
        except PlaceData.DoesNotExist:
            return None

def setPlaceRelation(fatherplace, sonplace):
    try:
        placeobj = PlaceRelations.objects.get(
                parentplace = fatherplace,
                sonplace = sonplace,
            )
        return placeobj
    except PlaceRelations.DoesNotExist:
        newplacerelation = PlaceRelations(
                parentplace = fatherplace,
                sonplace = sonplace,
            )
        newplacerelation.save()
        return newplacerelation

def getRelatedPlaceList(placeid):
    relatedlist = []
    placeobj = getPlaceData(placeid)
    if placeobj is None:
        return relatedlist
    try:
        relateddata = PlaceRelations.objects.filter(parentplace=placeobj)
        for eachdata in relateddata:
            relatedlist.append(eachdata.sonplace)
    except PlaceRelations.DoesNotExist:
        pass
    return relatedlist

def setItemData(itemname, itemimg, itemtype, itemstatus, desc=''):
    itemtypemst = getItemType(itemtype)
    if itemtypemst is None:
        print "no such type: %s" % (itemtype)
        return None
    itemstatusmst = getItemStatus(itemstatus)
    if itemstatusmst is None:
        print "no such status: %s" % (itemstatus)
        return None
    newItem = ItemData(
            itemname = itemname,
            itemimg = itemimg,
            itemtype = itemtypemst,
            itemstatus = itemstatusmst,
            itemdesc = desc,
        )
    newItem.save()
    return newItem

def getItemData(itemid=None):
    if itemid is None:
        try:
            allitem = ItemData.objects.all()
            return allitem
        except ItemData.DoesNotExist:
            return None
    try:
        itemobj = ItemData.objects.get(itemid = itemid)
        return itemobj
    except ItemData.DoesNotExist:
        return None

def updateItemData(itemid, itemname, itemimg, itemtype, itemstatus, desc=''):
    itemtypemst = getItemType(itemtype)
    if itemtypemst is None:
        print "no such type: %s" % (itemtype)
        return None
    itemstatusmst = getItemStatus(itemstatus)
    if itemstatusmst is None:
        print "no such status: %s" % (itemstatus)
        return None
    try:
        updateditem = ItemData.objects.filter(id=itemid)
        updateditem.update(
                itemname = itemname,
                itemimg = itemimg,
                itemtype = itemtypemst,
                itemstatus = itemstatusmst,
                itemdesc = desc,
            )
        return updateditem
    except ItemData.DoesNotExist:
        return setItemData(itemname, itemimg, itemtype)

def clearItem(itemid):
    try:
        clearitem = ItemData.objects.get(id=itemid)
        clearitem.delete()
    except ItemData.DoesNotExist:
        pass
    try:
        PlaceHoldItems.objects.filter(itemid=itemid).delete()
    except PlaceHoldItems.DoesNotExist:
        pass

def setItemInPlace(itemid, placeid):
    itemobj = getItemData(itemid)
    placeobj = getPlaceData(placeid)
    if itemobj and placeobj:
        try:
            checkobj = PlaceHoldItems.objects.get(
                    placedata = placeobj,
                    itemdata = itemobj,
                )
            return checkobj
        except PlaceHoldItems.DoesNotExist:
            newplaceitem = PlaceHoldItems(
                    placedata = placeobj,
                    itemdata = itemobj,
                )
            newplaceitem.save()
            return newplaceitem
    return None

def removeItemFromPlace(itemid, placeid):
    itemobj = getItemData(itemid)
    placeobj = getPlaceData(placeid)
    if itemobj and placeobj:
        try:
            data = PlaceHoldItems.objects.get(placedata=placeobj, itemdata=itemobj)
            data.delete()
            return True
        except PlaceHoldItems.DoesNotExist:
            return False

def initItemTypeData():
    typeall = getItemType()
    if typeall is not None and len(typeall) > 0:
        return
    setItemType('type1')
    setItemType('type2')
    setItemType('type3')
    setItemType('type4')

def initItemStatusData():
    statusall = getItemStatus()
    if statusall is not None and len(statusall) > 0:
        return
    setItemStatus('stored')
    setItemStatus('using')
    setItemStatus('lost')
    setItemStatus('dropped')

