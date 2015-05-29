#!/usr/bin/env python

#based almost entirely on GwynneR's excellent 'mm_MeshVolume.py' script,
#adapted to allow user-defined target volume

try:
    units = lx.eval('pref.value units.default ?')
    
    if (units!='millimeters' and units!='meters'):
        lx.eval('dialog.setup info')
        lx.eval('dialog.title {cj_scripts_scaleToVolume.py: units incorrect}')
        lx.eval('dialog.msg {This script only supports document units set to "millimeters" or "meters". "%s" are not supported.}' % units)
        lx.eval('dialog.open')
    
    else:
        currentLayer = lx.eval('query sceneservice selection ? mesh')
        if not isinstance(currentLayer, basestring):
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {cj_scripts_scaleToVolume.py: no funny business}')
            lx.eval('dialog.msg {Please select one mesh item to measure.}')
            lx.eval('dialog.open')
        else:

            # get selected layer
            layerID = lx.eval('query layerservice layer.ID ? selected')

            # triple and freeze polys on a new layer
            lx.eval('select.typeFrom polygon;edge;vertex;item;pivot;center;ptag true')
            lx.eval('copy')
            lx.eval('layer.new')
            lx.eval('paste')
            lx.eval('poly.freeze false')
            lx.eval('poly.triple')

            # ++++++++++++++++++++++++++++++++++++++++++++
            # BEGIN mm_MeshVolume.py +++++++++++++++++++++
            
            volume = 0
            # get default units
            magnitude = 1
            units = lx.eval('pref.value units.default ?')

            if units == 'micrometers':
                magnitude = 1000000
            elif units == 'millimeters':
                magnitude = 1000
            elif units == 'centimeters':
                magnitude = 100
            elif units == 'meters':
                magnitude = 1
            elif units == 'kilometers':
                magnitude = 0.001
            elif units == 'megameters':
                magnitude = 0.000001


            # get selected layer
            layerID = lx.eval('query layerservice layer.ID ? selected')

            # triple and freeze polys
            lx.eval('poly.freeze false')
            lx.eval('poly.triple')

            # get layer polys
            polys = lx.eval('query layerservice polys ? all')

            for poly in polys:
                znormal = lx.eval('query layerservice poly.normal ? %s' % poly)[2]

                if znormal == 0:
                    pass
                else:
                    if znormal > 0:
                        factor = 1.0
                    elif znormal < 0:
                        factor = -1

                    verts = lx.eval('query layerservice poly.vertList ? %s' % poly)
                    coords = {}

                    for index, vert in enumerate(verts):
                        coords[index] = lx.eval('query layerservice vert.wpos ? %s' % vert)

                    x1 = coords[0][0]
                    y1 = coords[0][1]
                    z1 = coords[0][2]

                    x2 = coords[1][0]
                    y2 = coords[1][1]
                    z2 = coords[1][2]

                    x3 = coords[2][0]
                    y3 = coords[2][1]
                    z3 = coords[2][2]

                    polyarea = 0.5*abs((x1*(y3-y2))+(x2*(y1-y3))+(x3*(y2-y1)))
                    vol = ((z1+z2+z3)/3.0)*polyarea

                    volume += (factor * vol)

            volume = volume * magnitude * magnitude * magnitude
            
            # END mm_MeshVolume.py +++++++++++++++++++++
            # ++++++++++++++++++++++++++++++++++++++++++
            
            if units == 'meters':
                litres = volume * (1000)
            elif units == 'millimeters':
                litres = volume / (1000000)
                
            if volume < 0.005:
                prettyVolume = '{0:.6g}'.format(round(volume,6))
            elif volume > 100000:
                prettyVolume = '{0:.10g}'.format(round(volume,-6))
            else:
                prettyVolume = '{0:.3g}'.format(volume)
                
            if litres < 0.005:
                litres = '%.8f' % litres
            else:
                litres = '%.3f' % litres
                
            lx.eval('layer.delete')
            lx.eval('select.item %s add' % currentLayer)
            
            lx.eval('dialog.setup yesNo')
            lx.eval('dialog.title {cj_scripts_scaleToVolume.py}')
            lx.eval('dialog.msg {mesh volume: %s cubic %s (%s L)\nScale to volume?}' % (prettyVolume, units, litres))
            lx.eval('dialog.open')
            
            yesNo = lx.eval('dialog.result ?')
            if yesNo == 'ok':
            
                # See if the user value exists
                if lx.eval("query scriptsysservice userValue.isDefined ? targetVolume")==0:
                    # Value doesn't exist; create it with calls to user.defNew
                    #  and user.def, and give it an initial value with
                    #  user.value
                    lx.eval( 'user.defNew targetVolume float' );
                    lx.eval( 'user.def targetVolume username \"Desired Volume (cc)\"' );
                    
                # See if a value has been set yet
                if lx.eval( "query scriptsysservice userValue.isSet ? targetVolume" )==0:
                    lx.eval('user.value targetVolume 1000' );
                    
                lx.eval('user.value targetVolume')
                targetVolume = lx.eval('user.value targetVolume ?')
                
                if units == 'millimeters':
                    targetVolume *= 10**3
                elif units == 'meters':
                    targetVolume *= 10**-6
                
                scaleFactor = (targetVolume/volume)**(.3333333333)
                
                lx.eval('tool.set TransformScale on')
                lx.eval('tool.setAttr xfrm.transform SX %s' % scaleFactor)
                lx.eval('tool.setAttr xfrm.transform SY %s' % scaleFactor)
                lx.eval('tool.setAttr xfrm.transform SZ %s' % scaleFactor)
                lx.eval('tool.doApply')
                lx.eval('tool.set TransformScale off 0')
           

except Exception, e:
    lx.out('%s line: %s' % (e, sys.exc_traceback.tb_lineno))
