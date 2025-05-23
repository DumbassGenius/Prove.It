from inspect import signature

ensure = True

emptyTypeDict = {dict: {}, list:[]}


def EnsureIsType(val, val_type: type):
    if ensure:
        if not (isinstance(val_type, type)):
            raise TypeError(val_type, "is not a type, is", type(val_type))
        if not isinstance(val, val_type):
            raise TypeError(val, "is not ", val_type, "is", type(val))
    return val

def Initiate(val, val_type):
    EnsureIsType(val_type, type)
    if val == None:
        return emptyTypeDict[val_type]
    else:
        EnsureIsType(val,val_type)
        return val
    

def EnsureIsListOf(val: list, val_type: type):
    if ensure:
        if not isinstance(val, (list, tuple)):
            raise TypeError(val, "is not a list, is", type(val))
        for element in val:
            EnsureIsType(element, val_type)
    return val

