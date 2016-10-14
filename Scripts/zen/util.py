#python

import defaults

def debug(string):
    if DEBUG:
        lx.out(string)

def random_color():
    import colorsys, random
    return colorsys.hsv_to_rgb(
        random.random(),
        defaults.get('random_color_saturation'),
        defaults.get('random_color_value')
    )

def build_arg_string(arg_dict):
    arg_string = ''
    for k,v in arg_dict.iteritems():
        if v is not None:
            v = str(v) if str(v).isalnum() else '{%s}' % str(v)
            arg_string += " %s:%s" % (str(k),v)
    return arg_string
