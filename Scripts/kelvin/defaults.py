#python

import modo, lx, lxu, symbols

MASK_GROUPS = [
    ("output","Outputs"),
    ("ignore","Overrides"),
    ("ptag","Polygons"),
    ("selset","Selection Sets"),
    ("part","Parts"),
    ("item","Items"),
    ("gloc","Folders"),
    ("group","Groups"),
    ("base","Default")
]

ENVIRONMENTS = [
    (
        "backplate",
        "Backplate",
        {
            lx.symbol.sICHAN_ENVIRONMENT_VISCAM: True,
            lx.symbol.sICHAN_ENVIRONMENT_VISIND: False,
            lx.symbol.sICHAN_ENVIRONMENT_VISREFL: False,
            lx.symbol.sICHAN_ENVIRONMENT_VISREFR: True,
            lx.symbol.sICHAN_ENVIRONMENT_RADIANCE: 1.0,
        }
    ),
    (
        "hdr",
        "HDR",
        {
            lx.symbol.sICHAN_ENVIRONMENT_VISCAM: False,
            lx.symbol.sICHAN_ENVIRONMENT_VISIND: True,
            lx.symbol.sICHAN_ENVIRONMENT_VISREFL: True,
            lx.symbol.sICHAN_ENVIRONMENT_VISREFR: True,
            lx.symbol.sICHAN_ENVIRONMENT_RADIANCE: 1.0,
        }
    )
    ]

DEFAULTS = {
    "ptag": 'Default',
    "name": 'untitled',
    "random_color_saturation": .7,
    "random_color_value": .95,
    "base_material_color": (.8,.8,.8),
    "mask_filter": lx.symbol.i_POLYTAG_MATERIAL,
    'material_channels':{
        lx.symbol.sICHAN_ADVANCEDMATERIAL_DIFFAMT: 0.8,
        lx.symbol.sICHAN_ADVANCEDMATERIAL_DIFFCOL: None,
        lx.symbol.sICHAN_ADVANCEDMATERIAL_SPECAMT: 0.04,
        lx.symbol.sICHAN_ADVANCEDMATERIAL_SMOOTH: True,
        lx.symbol.sICHAN_ADVANCEDMATERIAL_DBLSIDED: True
    },
    'shader_channels':{
        lx.symbol.sICHAN_DEFAULTSHADER_SHADERATE: 0.25,
    },
    'environment_channels':{
        lx.symbol.sICHAN_ENVIRONMENT_VISCAM: True,
        lx.symbol.sICHAN_ENVIRONMENT_VISIND: True,
        lx.symbol.sICHAN_ENVIRONMENT_VISREFL: True,
        lx.symbol.sICHAN_ENVIRONMENT_VISREFR: True,
        lx.symbol.sICHAN_ENVIRONMENT_RADIANCE: 1.0,
    },
    "default": False,
    "useLib": False,
}



def get_environments():
    """Returns the names of all environment items in the enforced kelvin shader tree structure."""
    return ENVIRONMENTS



def get_environment(key):
    """Returns the name of a single environment item in the enforced kelvin shader tree structure by key."""
    return [i for i in ENVIRONMENTS if i[0] == key]



def get_mask_groups():
    """Returns the names of all parent groups in the enforced kelvin shader tree structure."""
    return list_of_tuples_dump(MASK_GROUPS)



def get_mask_group(key):
    """Returns the name of a single parent group in the enforced kelvin shader tree structure by key."""
    return list_of_tuples_extract(key,MASK_GROUPS)



def list_of_tuples_dump(list_of_tuples):
    """Returns a list of values from a list of tuples e.g. [(key,value),(key1,value1)]
    """

    values = []
    for tuple_i in list_of_tuples:
        values.append(tuple_i[1])

    return values


def list_of_tuples_extract(key,list_of_tuples):
    """Returns a specific value from a list of tuples by key e.g. [(key,value),(key1,value1)]
    """

    for i in range(len(list_of_tuples)):
        if key == list_of_tuples[i][0]:
            return list_of_tuples[i][1]

    return False


def get(key):
    """Returns a default value for a given key."""
    return DEFAULTS[key]


def merge(overrides={},defaults=DEFAULTS):
    """Merges two objects recursively such that any elements existing in
    'overrides' are retained, and any missing elements will be replaced
    with those in 'defaults'. Useful for things like material channels,
    where the UI design may need to customize a specific channel, while
    leaving the rest at their default values.

    :param overrides: object containing override values
    :param defaults: object containing default values
    """

    result = defaults

    if isinstance(overrides,dict):
        for k,v in defaults.iteritems():
            if isinstance(v,list) or isinstance(v,dict) or isinstance (v,tuple):
                result[k] = merge(v,defaults[k])
            else:
                result[k] = overrides.get(k,result[k])

        for k,v in overrides.iteritems():
            if not hasattr(result,k):
                result[k] = v

    elif isinstance(overrides,list):
        for i in range(len(defaults)):
            try:
                result[i] = overrides[i]
            except:
                result[i] = defaults[i]

        for i in range(len(result),len(overrides)):
            result[i] = overrides[i]

    elif isinstance(overrides,tuple):
        result = overrides

    return result
