import sys

def bad_request(code=404, str='Not Found', msg=''):
    print('Status: %d %s' % (code, msg))
    print('Content-Type: text/html; charset=utf-8')
    print('Content-Length: %d' % len(msg))
    print(flush=True) 

    print(msg)

    sys.exit()