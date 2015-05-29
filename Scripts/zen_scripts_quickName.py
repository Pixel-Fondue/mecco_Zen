#python 

currentLayer = lx.eval('query sceneservice selection ? mesh')

if lx.eval("query scriptsysservice userValue.isDefined ? cj_tmp")==0:
    lx.eval( 'user.defNew cj_tmp string' );
    lx.eval( 'user.def cj_tmp username \"Add to mesh named:\"' );
    
meshName = lx.eval('user.value cj_tmp ?')

lx.eval('cut')
lx.eval('layer.new')
lx.eval('layer.renameSelected '+meshName)
lx.eval('paste')

lx.eval('select.item %s' % currentLayer)