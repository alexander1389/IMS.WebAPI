#!/usr/bin/python

import cgi
# import cgitb

from bad_request import bad_request
from report import report


def field_storage_to_dict(fs):
    """Get a plain dictionary from FieldStorage object

    :param fs: The FieldStorage object
    :type fs: FieldStorage
    :returns: Plain dictionary of FieldStorage parameters
    :rtype: dict
    """
    return {k: fs[k].value for k in fs.keys()}


# cgitb.enable()

actions = {
    'report': report
}

params = field_storage_to_dict(cgi.FieldStorage())
q = params['q'] if 'q' in params else None

if q in actions.keys():
    actions[q](**params)
else:
    bad_request(msg='Wrong Command')
