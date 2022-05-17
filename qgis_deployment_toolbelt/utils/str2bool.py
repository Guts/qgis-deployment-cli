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
    if isinstance(value, str):
        value = value.lower()
        if value in _true_set:
            return True
        if value in _false_set:
            return False

    if raise_exc:
        raise ValueError('Expected "%s"' % '", "'.join(_true_set | _false_set))
    return None
