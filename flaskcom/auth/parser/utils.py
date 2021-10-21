def convert_datatype(datatype):
    """TODO: Docstring for convert_datatype.
    Returns: TODO

    """
    if type(datatype) == unicode:
        return "varchar(255)"
    elif type(datatype) == type(int):
        return "int"
    else:
        datatype.converted_type

def convert_value(value):
    """TODO: Docstring for convert_value.

    Args:
        value (TODO): TODO

    Returns: TODO

    """
    if type(value) == unicode:
        return "\"{}\"".format(value)
    else:
        return value
