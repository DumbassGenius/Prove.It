from Expressions import *
from DefaultConstructions import *
from Contexts import *

types = {}

constructs = {}

def AddType(name, *parents):
    """
    Add a new type to the types dictionary.
    """
    if name in types:
        raise ValueError(f"Type {name} already exists.")
    
    # Ensure name only contains alphanumeric characters and underscores
    if not name.isidentifier():
        raise ValueError(f"Type name {name} is not valid. It should only contain alphanumeric characters and underscores.")

    # Create a new ExprType instance
    new_type = ExprType(name, *parents)
    
    # Add the new type to the types dictionary
    types[name] = new_type
    
    return new_type

def GetType(name):
    """
    Get a type from the types dictionary.
    """
    if name not in types:
        raise ValueError(f"Type {name} does not exist.")
    
    return types[name]

def BasicConstruct(name, inputTypes, outputType, renderString):
    """
    Add a basic construction to the constructs dictionary.
    """
    if name in constructs:
        raise ValueError(f"Construction {name} already exists.")
    
    
    # Ensure name only contains alphanumeric characters and underscores
    if not name.isidentifier():
        raise ValueError(f"Type name {name} is not valid. It should only contain alphanumeric characters and underscores.")

    inputTypes_objects = [GetType(type_name) for type_name in inputTypes]

    outputType = GetType(outputType)
    # Create a new Construct instance
    new_construct = Construct(renderString, defaultConstructionCreater(inputTypes_objects, outputType))
    
    # Add the new construct to the constructs dictionary
    constructs[name] = new_construct
    
    return new_construct

def Reset():
    """
    Reset the types and constructs dictionaries.
    """
    global types, constructs
    types = {}
    constructs = {}

def argSplitter(argString):
    """
    Splits a string of arguments into a list of arguments.
    Handles nested parentheses and commas.
    """
    args = []
    depth = 0
    current_arg = ""
    
    for char in argString:
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        
        if char == ',' and depth == 0:
            args.append(current_arg.strip())
            current_arg = ""
        else:
            current_arg += char
    
    if current_arg:
        args.append(''.join(current_arg).strip())
    
    return args


def textToExpr(text, context=None, expectingType=None):
    """
    Converts a textual representation of an expression into an Expr object.
    Constructs are created via their call: "#call(expr1, expr2, ...)".
    Variables are created via their type: "@type(symbol)".
    Identifiers in construct arguments are interpreted as the required type.
    """
    # Ensure a context exists
    if context is None:
        context = Context()

    # Handle variables (e.g., "@type(symbol)")
    if text.startswith("@"):
        type_and_symbol = text[1:].split("(")
        if len(type_and_symbol) != 2 or not type_and_symbol[1].endswith(")"):
            raise ValueError(f"Invalid variable format: {text}")
        type_name, symbol = type_and_symbol[0], type_and_symbol[1][:-1]
        if type_name not in types:
            raise ValueError(f"Unknown type: {type_name}")
        expr_type = types[type_name]
        return expr_type(symbol, context)

    # Handle constructs (e.g., "#call(expr1, expr2, ...)")
    elif text.startswith("#"):
        call_and_args = text[1:].split("(", 1)
        if len(call_and_args) != 2 or not call_and_args[1].endswith(")"):
            raise ValueError(f"Invalid construct format: {text}")
        call_name, args = call_and_args[0], call_and_args[1][:-1]
        if call_name not in constructs:
            raise ValueError(f"Unknown construct: {call_name}")
        construct = constructs[call_name]

        # Get the expected input types for the construct
        input_types = construct.construction.inputTypes if hasattr(construct.construction, 'inputTypes') else None

        arg_list = argSplitter(args)

        if input_types is None:
            input_types = [None] * len(arg_list)    
        elif len(arg_list) != len(input_types):
            raise ValueError(f"Expected {len(input_types)} arguments, but got {len(arg_list)}.")

        sub_exprs = [textToExpr(arg, context, input_types[i]) for i, arg in enumerate(arg_list)]
        print([sub_expr.type for sub_expr in sub_exprs])
        return construct(*sub_exprs)

    # Handle plain identifiers (if an expected type is provided)
    elif expectingType is not None and text.isidentifier():
        return expectingType(text, context)

    # If the format is invalid
    else:
        raise ValueError(f"Invalid expression format: {text}")
