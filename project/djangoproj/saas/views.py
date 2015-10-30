from saas.models import *

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

def addItemType(typename):
    try:
        typeobj = TypeMaster.objects.get(typename=typename)
        return typeobj
    except TypeMaster.DoesNotExist:
        newtypemst = TypeMaster(
                typename = typename,
            )
        newtypemst.save()
        return newtypemst

def updatePlaceData(placename, placeimg, imgrect):
    try:
        placeobj = PlaceData.objects.get(placename=placename)
        placeobj.update(placeimg=placeimg, imgrect=imgrect)
        return placeobj
    except PlaceData.DoesNotExist:
        newplacedata = PlaceData(
                placename = placename,
                placeimg = placeimg,
                imgrect = imgrect,
            )
        newplacedata.save()
        return newplacedata

def setPlaceRelation(fatherplace, sonplace):
    try:
        placeobj = PlaceRelations.objects.get(
                placeid = fatherplace,
                sonid = sonplace,
            )
        return placeobj
    except PlaceRelations.DoesNotExist:
        newplacerelation = PlaceRelations(
                placeid = fatherplace,
                sonid = sonplace,
            )
        newplacerelation.save()
        return newplacerelation

def addNewItem(itemname, itemimg, itemtype, itemstatus):
    newItem = ItemData(
            itemname = itemname,
            itemimg = itemimg,
            itemtype = itemtype,
            itemstatus = itemstatus,
        )
    newItem.save()
    return newItem

def updateItemInfo(itemid, itemname, itemimg, itemtype, itemstatus):
    try:
        updateditem = ItemData.objects.get(id=itemid)
        updateditem.update(
                itemname = itemname,
                itemimg = itemimg,
                itemtype = itemtype,
                itemstatus = itemstatus,
            )
        return updateditem
    except ItemData.DoesNotExist:
        return addNewItem(itemname, itemimg, itemtype)

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
    try:
        checkobj = PlaceHoldItems.objects.get(
                placeid = placeid,
                itemid = itemid,
            )
        return checkobj
    except PlaceHoldItems.DoesNotExist:
        newplaceitem = PlaceHoldItems(
                placeid = placeid,
                itemid = itemid,
            )
        newplaceitem.save()
        return newplaceitem

def removeItemFromPlace(itemid, placeid):
    try:
        target = PlaceHoldItems.objects.get(placeid=placeid, itemid=itemid)
        target.delete()
        return True
    except PlaceHoldItems.DoesNotExist:
        return False

def initPlaceData():
    currentdata = getPlaceData()
    if currentdata is None or len(currentdata) > 0:
        return False
    rootplace = updatePlaceData("house", "map.png", "")
    room = updatePlaceData("room", "", "0,0,512,512")
    if rootplace and room:
        setPlaceRelation(rootplace.id, room.id)

def getPlaceData(placeid=None):
    if placeid is None:
        try:
            allplace = PlaceData.objects.all()
            return allplace
        except PlaceData.DoesNotExist:
            return None
    else:
        try:
            specifyplace = PlaceData.objects.get(placeid=placeid)
            return specifyplace
        except PlaceData.DoesNotExist:
            return None
