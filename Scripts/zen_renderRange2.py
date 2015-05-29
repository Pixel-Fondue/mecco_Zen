#python
import re
from os import sep as pathSep
from os.path import expanduser
from time import sleep
from math import copysign


def exclog(script='batch render'):
    openLog()
    lx.out('Exception "%s" on line %d: %s' % (sys.exc_value, sys.exc_traceback.tb_lineno, script))


def openLog():
    eventLog_open = lx.eval("!layout.createOrClose EventLog \"Event Log_layout\" open:? title:@macros.layouts@EventLog@")
    if not eventLog_open:
        lx.eval("!layout.createOrClose EventLog \"Event Log_layout\" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true")


def getUserValue(name):
    #returns a user value
    #returns None if value does not exist
    try:
        exists = lx.eval("!query scriptsysservice userValue.isDefined ? {%s}" % name)
        if not exists or exists == "0":
            #user value does not exist; create it with default value
            return None
        else:
            #user value exists; return value
            value = lx.eval("!user.value {%s} ?" % name)
            return value
    except:
        exclog("function \"getUserName(%s)\"" % name)
        return None


def filterUniques(seq):
    #removes duplicates from input iterable
    seen = set()
    seen_add = seen.add
    return [x for x in seq if x not in seen and not seen_add(x)]


def filterNumerical(input):
    #removes any non-numerical characters
    #keeps dashes and periods for negatives
    #and floating point numbers
    numbers = "0123456789.-"
    if input:
        return "".join([c for c in input if c in numbers])
    else:
        return None


def parseError(rangeString):
    #outputs error message if parsing failed
    openLog()
    lx.out("No recognizable sequence info in \"%s\"" % rangeString)


def rangeFromString(inputString):
    """
    function:
        parses a string on the form "1, 5, 10-20:2" into a range like this:
        [1, 5, 10, 12, 14, 16, 18, 20]
        Filters out illegal stuff to it won't break if you make typos.
        Filters out duplicate frames, so "1, 1, 1, 1-5" will only output
        [1, 2, 3, 4, 5], rather than [1, 1, 1, 1, 2, 3, 4, 5]
    syntax:
        Commas divide up each "chunk".
        If there is a dash ("-") in a chunk, it gets treated as a range of frames.
        If there is also a colon (":") in the chunk, that number indicates the frame step.

        In the case of two colons present, like this: "2:0-100:3", the last one
        will take prescedence (the range becomes 0-100 step 3, not step 2).

        In the case of a colon but no dash, like this: "3:5", the colon is ignored and
        only the first number is parsed.

        To get a negative frame step (rendering 1-100, starting at 100), simply enter
        the large number first and the lower number after, like this: "100-1". Negative
        frame steps are ignored.
    output:
        returns a LIST object with INTEGERS for each frame in the range, in the same order
        they were entered. Does NOT SORT. This is easy to do once it's a list anyway:
            sortedList = rangeFromString(myRangeString).sort()
    """
    try:
        lx.out("Parsing render range: \"%s\"" % inputString)
        #first we clean up the string, removing any illegal characters
        legalChars = "0123456789-:, "
        cleanString = ""
        frames = []
        for char in inputString:
            if char in legalChars:
                cleanString += char

        rangeStrings = re.findall(r"[-0123456789:]+", cleanString) #splits up by commas and spaces
        for rangeString in rangeStrings:
            if "-" in rangeString[1:]:
                #is a sequence, so we need to parse it into a range

                #split up into start/end frames
                matchObject = re.search('\d-', rangeString)
                if matchObject:
                    splitIndex = matchObject.start()+1
                start, end = rangeString[:splitIndex], rangeString[splitIndex+1:]
                step = 1 #default value, can get overwritten by next two IF statements
                if ":" in start:
                    #check if there is a "step" setting
                    parts = start.split(":")
                    start = filterNumerical(parts[-1])
                    step = filterNumerical(parts[0])
                if ":" in end:
                    #check if there is a "step" setting
                    parts = end.split(":")
                    end = filterNumerical(parts[0])
                    step = filterNumerical(parts[-1])
                try:
                    start = int(start)
                    end = int(end)
                    step = int(step)
                except ValueError:
                    parseError(rangeString)
                    break #no recognizable sequence data here, so we skip this one

                step = max(abs(step), 1) #make sure that step isn't negative or zero

                if start>end:
                    step *= -1
                    sign = int(copysign(1, step))
                    first = max(start, end)
                    last = min(start, end)+sign
                else:
                    sign = int(copysign(1, step))
                    first = min(start, end)
                    last = max(start, end)+sign
                try:
                    thisRange = range(first, last, step)
                    frames.extend(thisRange)
                except:
                    parseError(rangeString) #skip this one


            else:
                #is a single frame; clean up, turn to an integer and append to list
                cleaned = re.split(r"\D", rangeString)
                try:
                    thisFrame = int(cleaned[0])
                    frames.append(thisFrame)
                except:
                    parseError(rangeString) #skip this one


        #we now have our list of frames, but it's full of duplicates
        #let's filter the list so each frame exists only once
        frames = filterUniques(frames)

        #All done! If frames, return frames, otherwise exit with error
        if frames:
            return frames
        else:
            parseError(inputString)
            return
    except:
        exclog()

def getRenderItem():
    #returns the ID of the render item
    return lx.eval("query sceneservice polyRender.id ? 0")

def checkOutputPaths():
    #utility function
    #returns True if there is at least one render output that is:
    #   Enabled, has an output path, an output format, and all its parents
    #   are enabled as well, and the top-level parent is the Render item

    n_renderOutputs = lx.eval("query sceneservice renderOutput.n ?")
    outputs = [lx.eval("query sceneservice renderOutput.id ? {%s}" % n) for n
                in range(n_renderOutputs)]
    for output in outputs:
        outputPath = lx.eval("item.channel filename ? item:{%s}" % output)
        outputFormat = lx.eval("item.channel format ? item:{%s}" % output)
        outputEnable = checkEnable(output)
        if all((outputPath, outputFormat, outputEnable)):
            return True
    return False


def checkEnable(texture):
    #iterates through shader tree parents of item "texture"
    #returns True if all shader tree parents are enabled; otherwise False
    #uses recursion to work its way through hierarchy

    enable = lx.eval("item.channel enable ? item:{%s}" % texture)
    if enable:
        thisParent = lx.eval("query sceneservice item.parent ? {%s}" % texture)
        thisParent_type = lx.eval("query sceneservice item.type ? {%s}" % thisParent)
        if thisParent_type == "polyRender":
            return True
        elif thisParent_type == "scene":
            return False
        else:
            return checkEnable(thisParent)
    else:
        return False


def setOrCreateUserValue(name, value, valueType="string", life="config", username=None):
    #sets a user value
    #if user value does not exist, it creates it first
    try:
        #first we try to just set the value
        #if it fails, it's probably because it does not exist
        lx.eval("!user.value {%s} {%s}" % (name, value))
        if username:
            lx.eval("!user.def name:{%s} attr:username value:{%s}" % (name, username))
    except:
        #it failed; probably does not exist
        #we try to create it and set it instead
        try:
            lx.eval("!user.defNew {%s} {%s} {%s}" % (name, valueType, life))
            lx.eval("!user.value {%s} {%s}" % (name, value))
        except:
            lx.out("Error creating user value:", name, valueType, life)
            exclog()
            return


def renderFrame(frame, useOutput=True, outputPath=None, outputFormat=None, clear=False, group=None):
    #renders a specific frame
    #            frame: Integer to choose frame
    #        useOutput: Boolean for using output controls from render outputs
    #       outputPath: String for output if useOutput is False
    #     outputFormat: String for output format if useOutput is False
    #            clear: Boolean, if True it will clear render on finish
    #NOTE: returns False if user aborted frame or if there is some error
    #      in the render process.
    #      returns True if frame completes without error.

    renderItem = getRenderItem()
    #start by reading previous values
    first = lx.eval("item.channel first ? item:{%s}" % renderItem)
    last = lx.eval("item.channel last ? item:{%s}" % renderItem)

    #then we set a single frame as the new range
    lx.eval("item.channel first %s item:{%s}" % (frame, renderItem))
    lx.eval("item.channel last %s item:{%s}" % (frame, renderItem))

    #then we figure out whether to use a render pass group or not
    if group:
        group = "group:{%s}" % group
    else:
        group = ""

    #then we render the current frame
    try:
        if useOutput:
            lx.eval("render.animation * * %s" % group)
        else:
            lx.eval("render.animation {%s} %s %s" % (outputPath, outputFormat, group))
    except:
        #error most likely because user aborted
        #restore frame range, and exit script
        lx.eval("item.channel first %s item:{%s}" % (first, renderItem))
        lx.eval("item.channel last %s item:{%s}" % (last, renderItem))
        lx.out("User aborted")
        return False #rendering failed, so we return False


    #if we complete the render, we restore the original frame range
    lx.eval("item.channel first %s item:{%s}" % (first, renderItem))
    lx.eval("item.channel last %s item:{%s}" % (last, renderItem))
    sleep(0.1)
    if clear:
        lx.eval("!render.clear")
    return True #rendering succeeded, so we return True




def renderRange(frames, group=None):
    #takes a list of ints as an argument
    #renders all frames in list

    #progress bars are disabled for now
    progressbarEnable = False

    #first we need to see if we have an output path in the render outputs:
    usePaths = False
    if checkOutputPaths():
        #there is a path set up for at least one render output, ask if we use it
        try:
            lx.eval("dialog.setup style:yesNo")
            lx.eval("dialog.title {Save Image Sequence}")
            lx.eval("dialog.msg {Use the filenames specified in the render outputs?}")
            lx.eval("dialog.open")
            lx.eval("dialog.result ?")
            usePaths = True
        except:
            #user pressed "no" -- don't do anything; usePaths stays False
            pass

    if not usePaths:
        #because usePaths is False, we must ask user for a file location
        try:
            #first we try to get previous values, and use defaults if that fails...
            try:
                #try user value
                previousPath = lx.eval("!user.value cj_renderPath ?")
            except:
                #No user value for previous path existed
                previousPath = lx.eval("query platformservice path.path ? project")
                if not previousPath:
                    #no project path, so we use scene path instead
                    scenePath = lx.eval("query sceneservice scene.file ? scene001")
                    if scenePath:
                        previousPath = scenePath.rsplit(pathSep, 1)[0]
                if not previousPath:
                    #no content path either, so we use user home directory
                    previousPath = expanduser("~")
                previousPath += pathSep
            try:
                #try user value
                previousFormat = lx.eval("!user.value cj_renderFormat ?")
            except:
                #No user value for previous format existed, default to 16-bit OpenEXR
                previousFormat = "openexr"


            #setting up dialog...
            lx.eval("dialog.setup fileSave")
            lx.eval("dialog.result {%s}" % previousPath)
            lx.eval("dialog.fileType image")
            lx.eval("dialog.fileSaveFormat {%s} format" % previousFormat)
            lx.eval("dialog.open")

            #getting results...
            filePath = lx.eval("dialog.result ?")
            fileFormat = lx.eval("dialog.fileSaveFormat ? format")
            fileExtension = lx.eval("dialog.fileSaveFormat ? extension")
            filePath = filePath.rsplit(".", 1)[0]

            #store output options in a user value...
            dirPath = filePath.rsplit(pathSep, 1)[0] + pathSep
            setOrCreateUserValue("cj_renderPath", dirPath)
            setOrCreateUserValue("cj_renderFormat", fileFormat)

        except:
            #error probably because user pressed "cancel"
            lx.out("User aborted")
            return
    else:
        #usePaths is True, so we don't need to get any file paths or anything
        pass

    lx.out("Rendering frames:")
    lx.out(frames)

    if progressbarEnable:
        progressbar = lx.Monitor(len(frames))
        progressbar.init(len(frames))
    for frame in frames:
        if frame == frames[-1]:
            clearFrame = False
        else:
            clearFrame = True
        if usePaths:
            if not renderFrame(frame, clear=clearFrame, group=group):
                break
                #slight strange syntax to safely catch aborted frames
        else:
            if not renderFrame(frame, False, filePath, fileFormat, clearFrame, group=group):
                break
        sleep(0.5)
        if progressbarEnable:
            progressbar.step(1)

def main():
    #main program

    try:
        #name for data user values
        rangeStringName = "cj_frameRangeStr"
        rangeStringName_user = "Render Range"
        renderPassEnableName = "cj_renderPassEnable"

        rangeString = getUserValue(rangeStringName)
        if not filterNumerical(rangeString):
            #rangeString didn't exist
            #create it with the current frame range as the default
            renderItem = getRenderItem()
            first = lx.eval("item.channel first ? item:{%s}" % renderItem)
            last = lx.eval("item.channel last ? item:{%s}" % renderItem)
            step = lx.eval("item.channel step ? item:{%s}" % renderItem)
            if not first == last:
                #is a range
                rangeStringNew = str(first) + "-" + str(last)
                if abs(step) > 1:
                    #has a step
                    rangeStringNew += ":" + str(step)
            else:
                #is not a range, just use a single value
                rangeStringNew = str(first)
            setOrCreateUserValue(rangeStringName, rangeStringNew, username=rangeStringName_user)
        try:
            lx.eval("user.value {%s}" % rangeStringName)
        except:
            lx.out("User aborted")
            return

        rangeString = getUserValue(rangeStringName)

        try:
            group = lx.eval("!group.current ? pass")
        except:
            group = None

        if group:
            groupName = lx.eval("query sceneservice item.name ? {%s}" % group)
            try:
                lx.eval("dialog.setup yesNo")
                lx.eval("dialog.title {Use render pass}")
                lx.eval("dialog.msg {Use render pass group  \"%s\"?}" % groupName)
                lx.eval("dialog.open")
                lx.out("Using current render pass group: \"%s\"" % groupName)
            except:
                group = None
        else:
            group = None

        frames = rangeFromString(rangeString)
        if frames:
            renderRange(frames, group)
        else:
            lx.eval("dialog.setup error")
            lx.eval("dialog.title Error")
            lx.eval("dialog.msg {No frame range recognized in \"%s\"}" % rangeString)
            lx.eval("dialog.open")
            return
    except:
        exclog("function main()")
        return

if __name__ == "__main__":
    main()
