__author__ = 'brianoneill'

def _execfile(filename, globs=None, locs=None):
    with open(filename) as f:
        code = compile(f.read(), "somefile.py", 'exec')
        exec(code, globs, locs)
