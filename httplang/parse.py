import utils
import sys

#preParse handles the loops and then feeds to parse function
#WARNING: NEED WAY TO HANDLE FORGOTTEN ENDLOOPS
def preParse(code,loops = 1):
    #fufill loops
    for i in range(loops):
        #loop state code
        loopDepth = 0
        rootLoopLength = 0
        loopCode = []
        #iterate through lines in the code
        for lineNumber, line in code:
            #set the global lines variables (add one because line count starts at one)
            utils.lines = lineNumber + 1
            splitLine = line.split()
            #ignore empty/blank lines
            if len(splitLine) > 0 or line == "\n":
                #handle loop begins
                if splitLine[0] == "loop":
                    #increase the loop depth
                    loopDepth += 1
                    #if this is the first/root loop, make this the rootLoopLength
                    if loopDepth == 1:
                        #check we have precisely one argument
                        if len(splitLine) != 2:
                            sys.exit("Loop Error, loop requires exactly one argument on line {0}".format(utils.lines))
                        #set rootLoopLength handling for non-ints
                        try:
                            rootLoopLength = int(splitLine[1])
                        except ValueError:
                            sys.exit("Loop error on line {0}. Loop amount must be integer not '{1}'.".format(utils.lines, splitLine[1]))
                    else:
                    #otherwise add this loop to the loop code
                        loopCode.append( (lineNumber,line) )
                #handle loop ends
                elif splitLine[0] == "endloop":
                    #handle if endloop has no corresponding loop
                    if loopDepth == 0:
                        sys.exit("Loop error on line {0}. endloop has no corresponding loop to begin from.".format(utils.lines, splitLine[1]))
                    #decrease loop depth
                    loopDepth -= 1
                    #parse the loopCode if this is the end of the rootLoop
                    if loopDepth == 0:
                        preParse(loopCode,rootLoopLength)
                        #clear the loop variables
                        loopCode = []
                    else:
                    #otherwise add it to the loop code
                        loopCode.append( (lineNumber,line) )
                else:
                    #if we are in a loop, add this line to the loop code
                    if loopDepth != 0:
                        loopCode.append( (lineNumber,line) )
                    else:
                    #otherwise go ahead and parse it
                        parse(line)

def parse(line):
    line = line.split()
    if line[0] in utils.keywords:
        utils.keywords[line[0]](line)
    else:
        sys.exit("Incorrect key word '{0}' on line {1}".format(line[0], utils.lines))

