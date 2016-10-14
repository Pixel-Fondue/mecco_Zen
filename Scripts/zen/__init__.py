#python

import lx, lxu, modo, traceback

DEBUG = True

try:
    import util
    import defaults
    import symbols
    import items
    import shadertree
    import selection
except:
    traceback.print_exc()
