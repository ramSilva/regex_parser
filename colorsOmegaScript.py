import os
import re

dir_path = os.path.dirname(os.path.realpath(__file__)) 

ignore = [
    "node_modules",
    "bower_components",
    "build/",
    "gen/",
    "output/",
    "mocks",
    "tests",
    "drawable"]

def singularPluralString(n, string):
    retValue = str(n) + " " + string
    if n != 1:
        retValue += "s"
    return retValue

def doStuff(regex):
    matches = 0
    filesList = {}
    colors = {}
    for root, dirs, files in os.walk(dir_path): 
        if not any(ext in root for ext in ignore):
            for file in files:
                if not any(ext in file for ext in ignore) and (file.endswith('.js')):
                    filePath = root + "/" + file
                    theFile = open(filePath)
                    theActualActualFile = theFile.read()
                    f = colorRe.findall(theActualActualFile)
                    if len(f) > 0:
                        filesList[filePath] = []
                        for match in f:
                            if match.upper() not in colors:
                                colors[match.upper()] = []
                            colors[match.upper()].append(filePath)
                            filesList[filePath].append(match.upper())
                            matches += 1
                            
                        theFile.close()
    return matches, filesList, colors

colorRe = re.compile("#[a-f0-9]{6,8}", re.I)

matches, filesList, colors = doStuff(colorRe)
print(str(matches) + " matches")
print("in " + str(len(filesList)) + " files")
print("\nUnique colors: " + str(len(colors)))

for color in colors:
    filesForColor = colors[color]
    uniqueFilesForColor = set(filesForColor)
    print("\n" + color + " defined " + singularPluralString(len(filesForColor), "time") + " in " + singularPluralString(len(uniqueFilesForColor), "file"))
    for file in uniqueFilesForColor:
        n = filesForColor.count(file)
        print(" " + singularPluralString(n, "time") + " in " + file)