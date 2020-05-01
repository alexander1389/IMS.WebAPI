import sys
import time

from os import listdir
from os.path import isfile, join, splitext, getctime, getsize, basename
from shutil import copyfileobj
from zipfile import ZipFile

from bad_request import bad_request
from utild import validate_dt


DEFAULT_EXT = '.xml'

def report(**kwargs):
    reply = get_reports_by_date('/tmp', '200301', '.pdf')

    return reply





# -------------------------------------------
# TODO: doc
def get_replist(path, ext = DEFAULT_EXT):
    return { f: time.strftime("%y%m%d%H%M%S", time.gmtime(getctime(f)))
        for f in (join(path, f) for f in listdir(path)) 
        if isfile(f) and splitext(f)[1] == ext }

def filter_by_date(lst, date):
    date = date.replace('_', '')

    if not lst or not date: 
        return []

    if not validate_dt(date):
        bad_request(400, 'Bad Request', 'Wrong Date')

    return [k for k, v in lst.items() if v[:len(date)] == date]

def get_reports_by_date(path, date, ext = DEFAULT_EXT):
    reports = filter_by_date(get_replist(path, ext), date)
    if not reports:
        bad_request(404, msg='No Reports')

    arch_name = 'rep_%s.zip' % date
    arch = ZipFile(arch_name, 'w')
    for report in reports:
        arch.write(report, basename(report))
    arch.close()

    print('Cache-Control: no-cache')
    print('Cache-Control: no-store')
    print('Content-Disposition: inline; filename="%s"' % arch_name)
    print('Content-Transfer-Encoding: binary')
    print('Content-Length: %d' % getsize(arch_name))
    print('Content-Type: application/zip')
    print(flush=True)
    
    with open(arch_name,'rb') as zipfile:
        copyfileobj(zipfile, sys.stdout.buffer)
# -------------------------------------------






# TODO: last cmd part


TEST_PATH = '/tmp'
if __name__ == '__main__':
    print("TEST...")

    d = get_replist(TEST_PATH, '.pdf')
    for k, v in d.items():
        print("%s - %s" % (k, v))

    l = filter_by_date(d, '2004')
    print('\nFOUND:\n')
    print(l)

    rep = get_reports_by_date(TEST_PATH, '2004', '.pdf')
    print(rep)
