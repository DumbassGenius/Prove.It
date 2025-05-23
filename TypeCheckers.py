ensure = True

empty_type_dict = {dict: {}, list: []}

def EnsureIsType(val, val_type: type):
    if ensure:
        if not isinstance(val_type, type):
            raise TypeError(f"{val_type} is not a type, is {type(val_type)}")
        if not isinstance(val, val_type):
            raise TypeError(f"{val} is not {val_type}, is {type(val)}")
    return val

def Initiate(val, val_type):
    EnsureIsType(val_type, type)
    if val is None:
        if val_type in empty_type_dict:
            if isinstance(empty_type_dict[val_type], dict):
                return {}
            elif isinstance(empty_type_dict[val_type], list):
                return []
        return None
    else:
        EnsureIsType(val, val_type)
        return val

def EnsureIsListOf(val: list, val_type: type):
    if ensure:
        EnsureIsType(val, list)
        for element in val:
            EnsureIsType(element, val_type)
    return val
