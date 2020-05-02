from datetime import datetime


def validate_dt(date):
    """ Validate datetime string

    :param date: The datetime string
    :type date: str
    :returns: True if the date is correct datetime string,
                False otherwise
    :rtype: bool
    """
    pattern = '000101000000'

    # letters in date
    if not date.isdecimal():
        return False

    # at least year must be specified
    if len(date) < 2 or len(date) > 12:
        return False

    if len(date) % 2 > 0:
        return False

    chk = date + pattern[len(date):]

    try:
        datetime.strptime(chk, '%y%m%d%H%M%S')
    except ValueError:
        return False

    return True


if __name__ == '__main__':
    print('\nDate Validator Check --- START')
    print('------------------------------\n')

    dates = [
        '99', '1312', '010212', '200229', '131024122203', '0',
        '03014', '01021312121222', '201301', '200230', '310131271212'
    ]

    for date in dates:
        print('%-15s - %s' % (date,
              'valid' if validate_dt(date) else 'invalid'))

    print('\n----------------------------')
    print('Date Validator Check --- END\n')
