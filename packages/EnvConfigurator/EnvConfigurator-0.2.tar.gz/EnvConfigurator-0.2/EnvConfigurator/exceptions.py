"""
    Custom Exceptions related to loading and parsing Environment Variable(s)
"""


class EnvVarNotFound(Exception):
    """
    Exception to throw when Environment Variable is not set properly.
    """
    pass


class EnvVarValueNotValid(Exception):
    """
    Exception to throw when Environment Variable's set value is valid
    as per provided criteria like in (var_type, optional, choices, separator)
    """
    pass
