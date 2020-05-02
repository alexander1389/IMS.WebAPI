import sys


def bad_request(code=404, str='Not Found', msg=''):
    """ Send error HTTP response

    :param code: The error code (optional (default=404))
    :type code: number
    :param str: The error message (optional (default='Not Found'))
    :type str: str
    :param msg: The extended error message in the body
                    of HTTP response (optional (default=''))
    """
    print('Status: %d %s' % (code, str))
    print('Content-Type: text/html; charset=utf-8')
    print('Content-Length: %d' % len(msg))
    print(flush=True)

    print(msg)

    sys.exit()
