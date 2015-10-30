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

def getItemType(typename):
    try:
        typeobj = TypeMaster.objects.get(typename=typename)
        return typeobj
    except TypeMaster.DoesNotExist:
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

def setItem(itemname, itemimg, itemtype, itemstatus, desc=''):
    newItem = ItemData(
            itemname = itemname,
            itemimg = itemimg,
            itemtype = itemtype,
            itemstatus = itemstatus,
            itemdesc = desc,
        )
    newItem.save()
    return newItem

def getItem(itemid):
    try:
        itemobj = ItemData.objects.get(itemid = itemid)
        return itemobj
    except ItemData.DoesNotExist:
        return None

def updateItem(itemid, itemname, itemimg, itemtype, itemstatus, desc=''):
    try:
        updateditem = ItemData.objects.filter(id=itemid)
        updateditem.update(
                itemname = itemname,
                itemimg = itemimg,
                itemtype = itemtype,
                itemstatus = itemstatus,
                itemdesc = desc,
            )
        return updateditem
    except ItemData.DoesNotExist:
        return setItem(itemname, itemimg, itemtype)

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
    itemobj = getItem(itemid)
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
    itemobj = getItem(itemid)
    placeobj = getPlaceData(placeid)
    if itemobj and placeobj:
        try:
            data = PlaceHoldItems.objects.get(placedata=placeobj, itemdata=itemobj)
            data.delete()
            return True
        except PlaceHoldItems.DoesNotExist:
            return False

def initPlaceData():
    currentdata = getPlaceData()
    if currentdata is None or len(currentdata) > 0:
        return False
    rootplace = setPlaceData("house", "house.png", "", "root")
    room = setPlaceData("room", "room.png", "0,0,512,512", "a room")
    if rootplace and room:
        setPlaceRelation(rootplace, room)
