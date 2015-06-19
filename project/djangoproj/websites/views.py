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
