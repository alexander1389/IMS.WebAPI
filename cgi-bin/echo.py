import sys


def echo(**kwargs):
    """ Return self argument in an HTTP response

    :param **kwargs: Parameters of GET request
    :type **kwargs: dict
    """
    msg = kwargs.get('msg', 'Hello, World!')

    print('Content-Type: text/html')
    print()
    print('<h1>%s</h1>' % msg)