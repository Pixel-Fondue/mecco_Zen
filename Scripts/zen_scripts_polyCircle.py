#python

# Get system units for conversion
def getSystemUnits():    
    unitSystem = lx.eval('pref.value units.system ?')
    defaultUnits = lx.eval('pref.value units.default ?')        
    units = magnitude = None
        
    #if unitSystem == "si":
    if defaultUnits == 'millimeters':
        units = 'mm'
        magnitude = 1000
        
    elif defaultUnits =="centimeters":
        units = 'cm'
        magnitude = 100
        
    elif defaultUnits == 'meters':
        units = 'm'
        magnitude = 1
        
    elif defaultUnits == 'micrometers':
        units = 'um'
        magnitude = 1000000
        
    elif defaultUnits == 'kilometers':
        units = 'km'
        magnitude = 0.001
        
    elif defaultUnits == 'megameters':
        units = 'Mm'
        magnitude = 0.000001
                
    #elif unitSystem == "english":
        
    if defaultUnits == 'feet':
        units = 'ft'
        magnitude = 3.2808399
        
    elif defaultUnits == 'inches':
        units = 'in'
        magnitude = 39.3700787
        
    elif defaultUnits == 'miles':
        units = 'mi'
        magnitude = 0.000621371192

    elif defaultUnits == 'mils':
        units = 'mil'
        magnitude = 39370.0787
            
    return units, magnitude

# See if the user value exists
if lx.eval("query scriptsysservice userValue.isDefined ? cj_prim_rad")==0:
    # Value doesn't exist; create it with calls to user.defNew
    #  and user.def, and give it an initial value with
    #  user.value
    lx.eval( 'user.defNew cj_prim_rad distance' );
    lx.eval( 'user.def cj_prim_rad username \"Radius\"' );
    
    
# See if a value has been set yet
if lx.eval( "query scriptsysservice userValue.isSet ? cj_prim_rad" )==0:
    lx.eval('user.value cj_prim_rad "1m"' );
    
lx.eval('user.value cj_prim_rad')
cj_prim_rad = lx.eval('user.value cj_prim_rad ?')
                
currentLayer = lx.eval('query sceneservice selection ? mesh')
if not isinstance(currentLayer, basestring):
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {cj_scripts_polyCircle.py: no funny business}')
    lx.eval('dialog.msg {Please select one mesh item in which to create the circle.}')
    lx.eval('dialog.open')
else:

    # get selected layer
    layerID = lx.eval('query layerservice layer.ID ? selected')

    # triple and freeze polys on a new layer
    #lx.eval('select.typeFrom polygon;edge;vertex;item;pivot;center;ptag true')

    lx.eval('layer.new')
                
    lx.eval( 'tool.set prim.cylinder on' )
    lx.eval( 'tool.setAttr prim.cylinder cenX 0' )
    lx.eval( 'tool.setAttr prim.cylinder cenY 0' )
    lx.eval( 'tool.setAttr prim.cylinder cenZ 0' )
    lx.eval( 'tool.setAttr prim.cylinder sizeX %s' % cj_prim_rad )
    lx.eval( 'tool.setAttr prim.cylinder sizeY %s' % 0 )
    lx.eval( 'tool.setAttr prim.cylinder sizeZ %s' % cj_prim_rad )
    lx.eval( 'tool.doApply' )
    
    u, m = getSystemUnits()
    
    lx.eval('select.type polygon')
    lx.eval( 'select.all' )
    bevelWidth = (cj_prim_rad/4)
    lx.eval( 'tool.set poly.bevel on' )
    lx.eval( 'tool.setAttr poly.bevel inset %s' % bevelWidth )
    lx.eval( 'tool.doApply' )
    lx.eval( 'delete' )
    
    lx.eval('cut')
    lx.eval('layer.delete')
    lx.eval('select.item %s add' % currentLayer)
    lx.eval('paste')