# -*- coing: utf-8 -*-
from __future__ import unicode_literals, division

# A m21 B 12m C
from collections import defaultdict


def text_parser(s):
    """

    :param s: list of strings like A -> B -> C
    :return: A dict that holds information about tables and foreign keys
    """
    result = defaultdict(list)
    for sub_s in:
        tables = s.replace(" ", "").split("->")
        for i, table in enumerate(tables):
            try:
                result[table].append(tables[i+1])
            except IndexError:
                pass

    return result

