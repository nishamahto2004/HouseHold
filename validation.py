
def empty(dataList):
    for d in dataList:
        if d=='':
            return True
        

def checkdigit(data):
    if(data.isdigit()):
        return False
    else:
        return True
    
def checkalpha(data):
    if(data.isalpha()):
        return False
    else:
        return True
        