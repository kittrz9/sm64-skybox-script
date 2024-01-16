#!/bin/env python

# either put this script somewhere that your PATH environment variable points to
# so you can just call this script in any decomp project
# 
# or put this in the tools directory of your decomp project
# and call it like ./tools/add_skybox.py while in that project

import sys
import os

def main():
    if len(sys.argv) == 1 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(f"Usage: {sys.argv[0]} custom_skybox_filename\n\nYour custom skybox texture must already be in ./textures/skyboxes/\nYou must run this script in your desired decomp directory")
        return

    verbose = False
    if "-v" in sys.argv:
        verbose = True

    # to get the file's name even if it has .png after it
    skyboxName = os.path.splitext(sys.argv[1])[0]
    skyboxID = "BACKGROUND_" + skyboxName.upper()
    
    if not os.path.exists("./textures/skyboxes/" + skyboxName + ".png"):
        print(f"File {sys.argv[1]} does not exist")
        return

    if not os.path.exists("./src/game/skybox.c"):
        print(f"This script seems to not be executed within any sm64 decomp folder\nPlease fix that")
        return


    # add the ptrlist extern to the file
    # probably doesn't need to be in the right spot but whatever
    f = open("./src/game/skybox.c", mode='r')
    lines = f.readlines()
    f.close()

    # check if this script has already modified this file
    if [l for l in lines if f"{skyboxName}_skybox_ptrlist" in l]:
        print(f"Skybox \"{skyboxName}\" found in src/game/skybox.c, aborting")
        return

    firstExternIndex = [i for i in range(0, len(lines)) if "extern SkyboxTexture" in lines[i]][0]
    lastExternIndex = [i for i in range(firstExternIndex, len(lines)) if lines[i] == "\n"][0]

    lines.insert(lastExternIndex, f"extern SkyboxTexture {skyboxName}_skybox_ptrlist;\n")

    # update the skybox textures array
    sSkyboxTexturesIndex = [i for i in range(0, len(lines)) if "SkyboxTexture *sSkyboxTextures[" in lines[i]][0]

    # make the array not fixed length if it isn't already
    lines[sSkyboxTexturesIndex] = "SkyboxTexture *sSkyboxTextures[] = {\n"

    # find the end of the array and add new skybox to the end
    arrayEndIndex = [i for i in range(sSkyboxTexturesIndex+1, len(lines)) if "};" in lines[i]][0]
    
    lines.insert(arrayEndIndex, f"    &{skyboxName}_skybox_ptrlist,\n")

    if verbose:
        print("---START OF SRC/GAME/SKYBOX.C---")
        for line in lines:
            print(line, end="")
        print("---END OF SRC/GAME/SKYBOX.C---")
    f = open("src/game/skybox.c", mode='w')
    f.writelines(lines)
    f.close()


    f = open("./include/geo_commands.h", mode='r')

    lines = f.readlines()

    # check if this file has been modified too
    if [l for l in lines if f"{skyboxID}" in l]:
        print(f"Skybox \"{skyboxName}\" found in include/geo_commands.h, aborting")
        return

    # maybe I don't need to actually find the enum declaration since it's the first in the file and I can just find the first "};"
    # but I feel like I should anyway in case the user modifies this file
    # I also probably don't need to put these in the end of the thing, but I want it to be tidy
    
    skyboxEnumStartIndex = [i for i in range(0, len(lines)) if "enum SkyBackgroundParams {" in lines[i]][0]
    skyboxEnumEndIndex = [i for i in range(skyboxEnumStartIndex, len(lines)) if "};" in lines[i]][0]

    # for some reason decomp doesn't put a comma at the end of the enum here
    # so I gotta fix it myself lmao
    # not hard coding it to always add a comma incase this file's already been modified
    for i in range(skyboxEnumStartIndex+1, skyboxEnumEndIndex):
        if not lines[i].endswith(",\n"):
            lines[i] = lines[i].rstrip("\n") + ",\n"


    lines.insert(skyboxEnumEndIndex, f"    {skyboxID},\n")
    
    
    if verbose:
        print("---START OF INCLUDE/GEO_COMMANDS.H---")
        for line in lines:
            print(line, end="")
        print("---END OF INCLUDE/GEO_COMMANDS.H---")
    f = open("include/geo_commands.h", mode='w')
    f.writelines(lines)
    f.close()

    # time for funny segment shenanigans

    f = open("include/segment_symbols.h", mode='r')
    lines = f.readlines()

    if [l for l in lines if f"DECLARE_SEGMENT({skyboxName}_skybox" in l]:
        print(f"Skybox \"{skyboxName}\" found in include/segment_symbols.h, aborting")
        return

    declareSegmentStart = [i for i in range(0, len(lines)) if "DECLARE_SEGMENT(water_skybox_mio0)" in lines[i]][0]
    declareSegmentEnd = [i for i in range(declareSegmentStart, len(lines)) if lines[i] == "\n"][0]

    lines.insert(declareSegmentEnd, f"DECLARE_SEGMENT({skyboxName}_skybox_mio0)\n")

    if verbose:
        print("---START OF INCLUDE/SEGMENT_SYMBOLS.H---")
        for line in lines:
            print(line, end="")
        print("---END OF INCLUDE/SEGMENT_SYMBOLS.H---")
    f = open("include/segment_symbols.h", mode='w')
    f.writelines(lines)
    f.close()


    f = open("./sm64.ld", mode='r')
    lines = f.readlines()

    if [l for l in lines if f"YAY0_SEG({skyboxName}_skybox" in l]:
        print(f"Skybox \"{skyboxName}\" found in sm64.ld, aborting")
        return

    linkerSegmentStart = [i for i in range(0, len(lines)) if "YAY0_SEG(water_skybox," in lines[i]][0]
    linkerSegmentEnd = [i for i in range(linkerSegmentStart, len(lines)) if lines[i] == "\n"][0]

    lines.insert(linkerSegmentEnd, f"   YAY0_SEG({skyboxName}_skybox,        0x0A000000)\n")

    if verbose:
        print("---START OF SM64.LD---")
        for line in lines:
            print(line, end="")
        print("---END OF SM64.LD---")
    f = open("sm64.ld", mode='w')
    f.writelines(lines)
    f.close()

    print(f"The skybox should now be added\nPlease set your Fast64 level's background to custom and set its ID to \"{skyboxID}\" and its background segment to \"{skyboxName}_skybox\"")
    



if __name__ == "__main__":
    main()

# MIT License
# 
# Copyright (c) 2024 kittrz
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



