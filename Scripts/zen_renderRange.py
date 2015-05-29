#python
import re

if lx.eval("query scriptsysservice userValue.isDefined ? cj_frameRangeStr")==0:
    lx.eval( 'user.defNew cj_frameRangeStr string' );
    lx.eval( 'user.def cj_frameRangeStr username \"frames to render:\"' );

# if lx.eval("query scriptsysservice userValue.isDefined ? cj_renderPath")==0:
    # lx.eval( 'user.defNew cj_renderPath string' );
    # lx.eval( 'user.def cj_renderPath username \"default render path:\"' );
        
# lx.eval("dialog.setup fileSave")
# lx.eval("dialog.fileType {image}")
# lx.eval("dialog.fileSaveFormat {openexr_32}")
# lx.eval("dialog.msg {select render path}")
# lx.eval("dialog.open")
# renderPath = lx.eval('dialog.result ?')
# renderPath = re.sub(r'/(.*)\.[^.]+$/','',renderPath)
# lx.eval('user.value cj_renderPath {%s}' % renderPath)
    
lx.eval('user.value cj_frameRangeStr')

frameRangeStr = lx.eval('user.value cj_frameRangeStr ?')
originalFrameRate = lx.eval('time.fps ?')


# I suck at regex, so cut me some slack... it works:

# 1) Remove anything that's not 0-9, comma or space
frameRangeStr = re.sub(r'[^0-9-, ]','',frameRangeStr)
# 2) Replace all spaces with commas (will allow multiple commas if a space is between them, hence step 3)
frameRangeStr = re.sub(r' *,+ *| +',',',frameRangeStr)
# 3) Replace all multi-commas with single commas
frameRangeStr = re.sub(r',+',',',frameRangeStr)
# 4) Remove all leading zeros (0000101 => 101, 0000 -> 0)
# plain English: matches zero or more zeros that are (a) at the beginning of the string and (b) followed by 0-9
frameRangeStr = re.sub(r'(^0*)(?=[0-9])','',frameRangeStr)

frameRangeStrList = frameRangeStr.split(',')
frameRangeIntList = []

for chunk in frameRangeStrList:
    if '-' in chunk:
        rangeList = chunk.split('-')
        if int(rangeList[0]) < int(rangeList[1]):
            for i in range(int(rangeList[0]),int(rangeList[1])+1):
                frameRangeIntList.append(str(i))
        else:
            for i in range(int(rangeList[0]),int(rangeList[1])-1,-1):
                frameRangeIntList.append(str(i))
    else:
        frameRangeIntList.append(str(chunk))
        
frameRangeIntListAsString = ','.join(frameRangeIntList)
        
try:
    lx.eval('time.fpsCustom 24')

    #lx.eval("dialog.setup info")
    #lx.eval("dialog.msg {frames: %s}" % (frameRangeIntListAsString))
    #lx.eval("dialog.open")
    
    for i in frameRangeIntList:
        time = float(i) / 24
        
        # lx.eval("dialog.setup info")
        # lx.eval("dialog.msg {now rendering frame %s\ntime: %s}" % (i,time))
        # lx.eval("dialog.open")
        
        lx.eval('select.time %s' % time)
        lx.eval('render.animationDialog %s %s 1 sequence {}' % (i,i))
        
    lx.eval('time.fps %s' % originalFrameRate)
        
except Exception,e:
    lx.out('Oh my, something\'s gone terribly wrong.')
    lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true')