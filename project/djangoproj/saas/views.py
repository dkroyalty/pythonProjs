from saas.models import TaxStandard

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
