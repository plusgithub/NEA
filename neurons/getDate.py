from datetime import datetime

def getDate(object):
    now = datetime.now()
    datenow = now.strftime("%d/%m/%Y")
    return(datenow)