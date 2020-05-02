import sys
import time

from datetime import datetime
from os import listdir, stat
from os.path import isfile, join, splitext, getsize, basename
from shutil import copyfileobj
from zipfile import ZipFile

from bad_request import bad_request
from utils import validate_dt

DEFAULT_EXT = '.xml'

def report(**kwargs):
    #reply = get_reports_by_date('/tmp', '200301', '.pdf')

    reply = get_last_report('/tmp', '.txt')

    return reply





# -------------------------------------------
def get_ctime(path):
    """ Get file creation time 

    :param path: The file location path
    :type path: str
    :returns: a file creation time (or last modified time if ctime getting fails on *nix)
    :rtype: str
    """
    st_info = stat(path)
    try:
        t = st_info.st_birthtime
    except AttributeError:
        t = st_info.st_mtime

    return datetime.fromtimestamp(t).strftime("%y%m%d%H%M%S")

def get_replist(path, ext = DEFAULT_EXT):
    """ Get a list of reports (non-recursively)

    :param path: The location of reports
    :type path: str
    :param ext: The extension of reports files (optional (default=DEFAULT_EXT))
    :type ext: str
    :returns: a dictionary containing pairs of absolute filename and creation time of the report
    :rtype: dict
    """
    return { f: get_ctime(f) for f in (join(path, f) for f in listdir(path)) 
             if isfile(f) and splitext(f)[1] == ext }

def filter_by_date(lst, date):
    """ Filter reports list by date

    :param lst: Reports dictionary
    :type lst: dict
    :param date: Date to filter by
    :type date: str
    :returns: list of absolute filenames of reports corresponding to the date
    :rtype: list
    """
    date = date.replace('_', '')

    if not lst or not date: 
        return []

    if not validate_dt(date):
        bad_request(400, 'Bad Request', 'Wrong Date')

    return [k for k, v in lst.items() if v[:len(date)] == date]

def get_reports_by_date(path, date, ext = DEFAULT_EXT):
    """ Get reports filtered by date in an HTTP response

    :param path: The location of reports
    :type path: str
    :param date: Date to get reports by
    :type date: str
    :param ext: The extension of reports files (optional (default=DEFAULT_EXT))
    :type ext:str
    """
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
    print('Content-Disposition: attachment; filename="%s"' % arch_name)
    print('Content-Transfer-Encoding: binary')
    print('Content-Length: %d' % getsize(arch_name))
    print('Content-Type: application/zip')
    print(flush=True)
    
    with open(arch_name,'rb') as zipfile:
        copyfileobj(zipfile, sys.stdout.buffer)

def get_last_report(path, ext = DEFAULT_EXT):
    """ Get last created report in an HTTP response

    :param path: The location of report
    :type path: str
    :param ext: The extension of report file (optional (default=DEFAULT_EXT))
    :type ext:str
    """
    lst = get_replist(path, ext)
    if not lst:
        bad_request(404, msg='No Reports')

    last_report = sorted(lst.items(), key=lambda x: (x[1], x[0]), reverse=True)[0][0]
    report_name = basename(last_report)

    print('Cache-Control: no-cache')
    print('Cache-Control: no-store')
    print('Content-Disposition: attachment; filename="%s"' % report_name)
    print('Content-Transfer-Encoding: binary')
    print('Content-Length: %d' % getsize(last_report))
    print('Content-Type: application/octet-stream')
    print(flush=True)
    
    with open(last_report,'rb') as file:
        copyfileobj(file, sys.stdout.buffer)

# -------------------------------------------



TEST_PATH = '/tmp'
if __name__ == '__main__':
    print("TEST...")
    """
    d = get_replist(TEST_PATH, '.pdf')
    for k, v in d.items():
        print("%s - %s" % (k, v))

    l = filter_by_date(d, '2004')
    print('\nFOUND:\n')
    print(l)

    rep = get_reports_by_date(TEST_PATH, '2004', '.pdf')
    print(rep)
    """
    get_last_report(TEST_PATH, '.txt')
