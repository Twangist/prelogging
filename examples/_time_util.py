__author__ = 'brianoneill'

#----------------------------------------------------------------------------
# elapsed time in secs to human-readable time
# Adapted from
# http://snipplr.com/view/5713/python-elapsedtime-human-readable-time-span-given-total-seconds/
#----------------------------------------------------------------------------
def elapsed_time_human_readable(seconds, suffixes=('y', 'w', 'd', 'h', 'm', 's'), sep=' '):
    """Takes an amount of seconds and turns it into a human-readable amount of time."""
    # The parts of the formatted time string to be returned
    time_list = []

    # the parts of time to iterate over (years, weeks, days, hours, minutes, seconds)
    # - the first item in each tuple is the suffix (y, w, d, h, m, s)
    # - the second is the length of such a unit in seconds (e.g. a day is 60s/m * 60m/h * 24h)
    parts = [
        (suffixes[0], 60 * 60 * 24 * 7 * 52),
        (suffixes[1], 60 * 60 * 24 * 7),
        (suffixes[2], 60 * 60 * 24),
        (suffixes[3], 60 * 60),
        (suffixes[4], 60),
    #   (suffixes[5], 1)
    ]

    # for each time part, grab the value and remaining seconds, and add it to
    # the time string
    for suffix, length in parts:
        value = int(seconds // length)
        if value > 0:
            seconds = seconds % length
            time_list.append('%s%s' % (str(value), suffix))
        if seconds < 1:
            break
    secs_hundredths = '{:.2f}{:s}'.format(seconds, suffixes[5])
    if secs_hundredths[:4] != '0.00':
        time_list.append(secs_hundredths)

    return sep.join(time_list) if time_list else '< 0.01s'
