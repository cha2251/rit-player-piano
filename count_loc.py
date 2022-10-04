import os

CODE_FILE_WHITELIST = ['.py', '.js', '.html', '.css']

def getNumberOfLinesInFile(filepath):
    return sum(1 for line in open(filepath, 'r'))

def countLinesOfCode():
    totalLinesOfCode = 0

    for path, subdirs, files in os.walk('.'):
        for filename in files:
            if any(filename.endswith(extension) for extension in CODE_FILE_WHITELIST):
                filepath = os.path.join(path, filename)
                linesOfCode = getNumberOfLinesInFile(filepath)

                totalLinesOfCode += linesOfCode

    print('Total lines of code: {} ({} kLOC)'.format(totalLinesOfCode, totalLinesOfCode // 1000))

if __name__ == '__main__':
    countLinesOfCode()