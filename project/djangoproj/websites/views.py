from websites.models import Websites

def getOrderedWebList():
    try:
        weblist = Websites.objects.all()
    except Websites.DoesNotExist:
        return None
    return weblist

def saveNewWebsite(seq, website, desc, detail):
    newsite = Websites(
            webseq = seq,
            website = website,
            desc = desc,
            detail = detail,
        )
    newsite.save()
    return newsite

def deleteWebsiteBySeq(seq):
    record = Websites.objects.get(webseq=seq)
    try:
        record.delete()
    except:
        return False
    return True

def clearWebsites():
    record = Websites.objects.all.delete()
    return (len(getOrderedWebList()) == 0)
