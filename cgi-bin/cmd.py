#!/usr/bin/python

import cgi
import cgitb

cgitb.enable()

from bad_request import bad_request
from report import report

actions = { 
    'report' : report
}

if __name__ == '__main__':
    form = cgi.FieldStorage()

    q = form['q'].value if 'q' in form else None

    reply = actions[q]() if q in actions.keys() else bad_request() # TODO: rv + bad_req param + actions param
