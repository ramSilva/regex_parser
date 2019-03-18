import os
import re
import argparse

defaultExclude = [
    "node_modules",
    "bower_components",
    "build/",
    "gen/",
    "output/",
    "mocks",
    "tests",
    "drawable"]

parser = argparse.ArgumentParser(
    description="Find repeated definitions for a given regex and tag them per file.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "dir",
    help="Directory to search.")
parser.add_argument(
    "include",
    help="File types to include",
    nargs="+",
    type=str)
parser.add_argument(
    "-e", "--exclude",
    help="List of paths/files to exclude.",
    metavar="Exclude",
    dest="exclude",
    type=str,
    default=[],
    nargs="*")
parser.add_argument(
    "-d", "--default_exclude",
    help="Use default exclude values for file paths and names. Can be used in conjunction with -e",
    action="store_true")
parser.add_argument(
    "-r", "--regex",
    help="Regex to search for. Defaults to hexadecimal color search",
    metavar="regex",
    dest="regex",
    type=str,
    default="#[a-fA-F0-9]{6,8}",)

args = parser.parse_args()
dir_path = args.dir

exclude = args.exclude
if args.default_exclude:
    exclude.extend(defaultExclude)

include = args.include
regex = args.regex

def singularPluralString(n, string):
    retValue = str(n) + " " + string
    if n != 1:
        retValue += "s"
    return retValue

def search(regex):
    filesList = {}
    matches = {}
    n = 0
    for root, dirs, files in os.walk(dir_path): 
        if not any(ext in root for ext in exclude):
            for file in files:
                if (not any(ext in file for ext in exclude)) and any(file.endswith(ext) for ext in include):
                    filePath = root + "/" + file
                    theFile = open(filePath)
                    fileContent = theFile.read()
                    f = regex.findall(fileContent)
                    if len(f) > 0:
                        filesList[filePath] = []
                        for match in f:
                            if match.upper() not in matches:
                                matches[match.upper()] = []
                            matches[match.upper()].append(filePath)
                            filesList[filePath].append(match.upper())
                            n += 1
                    theFile.close()
    return filesList, matches, n

compiledRegex = re.compile(regex)

filesList, matches, n = search(compiledRegex)
print(str(n) + " matches")
print("in " + str(len(filesList)) + " files")
print("\nUnique matches: " + str(len(matches)))

for match in matches:
    filesForMatch = matches[match]
    uniqueFilesForMatch = set(filesForMatch)
    print("\n" + match + " defined " + singularPluralString(len(filesForMatch), "time") + " in " + singularPluralString(len(uniqueFilesForMatch), "file"))
    for file in uniqueFilesForMatch:
        n = filesForMatch.count(file)
        print(" " + singularPluralString(n, "time") + " in " + file)