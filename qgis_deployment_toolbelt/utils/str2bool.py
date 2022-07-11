#! python3  # noqa: E265

"""
    Basic string to bool.
"""

# #############################################################################
# ########## Globals ###############
# ##################################

_true_set = {"on", "t", "true", "y", "yes", "1"}
_false_set = {"f", "false", "n", "no", "off", "0"}


# #############################################################################
# ########## Functions #############
# ##################################
def str2bool(value: str, raise_exc: bool = False) -> bool:
    """Determine if a string is a bool and, if so, convert it.

    :param str value: value to convert
    :param bool raise_exc: strict mode, defaults to False
    :raises ValueError: value is not in true and false sets

    :return bool: True if input string is in _true_set, False if it's in _false_set.
    None or Exception if not in any of two sets.
    """
    if isinstance(value, str):
        value = value.lower()
        if value in _true_set:
            return True
        if value in _false_set:
            return False

        if raise_exc:
            raise ValueError('Expected "%s"' % '", "'.join(_true_set | _false_set))

        return None
    else:
        raise TypeError(f"value must be a str, not {type(value)}")
