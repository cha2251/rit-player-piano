#!/usr/bin/python3

import os

SEARCH_DIRECTORIES = ['page', 'tools', 'src', 'test'] # What directories to recursively search
CODE_FILE_WHITELIST = ['.py', '.js', '.html', '.css']

def getNumberOfLinesInFile(filepath):
    return sum(1 for line in open(filepath, 'r'))

def countLinesOfCodeInRoot(root):
    totalLinesOfCode = 0

    for path, subdirs, files in os.walk(root):
        for filename in files:
            if any(filename.endswith(extension) for extension in CODE_FILE_WHITELIST):
                filepath = os.path.join(path, filename)
                linesOfCode = getNumberOfLinesInFile(filepath)

                print("\"{}\" has {} lines".format(filepath, linesOfCode))

                totalLinesOfCode += linesOfCode

    return totalLinesOfCode

def countLinesOfCode():
    totalLinesOfCode = 0

    for dir in SEARCH_DIRECTORIES:
        searchDir = os.path.join('..', dir)
        totalLinesOfCode += countLinesOfCodeInRoot(searchDir)

    print('\nTotal lines of code: {} ({:.2f} kLOC)'.format(totalLinesOfCode, totalLinesOfCode / 1000))

if __name__ == '__main__':
    countLinesOfCode()