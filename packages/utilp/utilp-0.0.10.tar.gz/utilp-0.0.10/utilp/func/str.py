"""String utility functions for Python 3."""

import re


def str_replace_by_dict(string: str, rep_dict: dict) -> str:
    """Replaces multiple source-destination substrings by a given dict.

    Parameters
    ----------
    string : str
        The string to replace substrings in.
    rep_dict : dict
        A dictionary of source-destination mappings to use for replacement.

    Returns
    -------
    str
        The resulting string after substring replacements.

    Example
    -------
        >>> rep_dict = {'cat': 'dog', 'a': 'b'}
        >>> str_replace_by_dict('my cat is a friend', rep_dict)
        'my dog is b friend'
    """
    rep = dict((re.escape(k), v) for k, v in rep_dict.items())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], string)
