#!/usr/bin/env python3
import sys
import os

class Squash_PlainText:
    def Name(self):
        return 'PlainText'

    def Compress(self, words):
        return 'print("Not yet implemented.")'

AlgorithmList = [
    Squash_PlainText()
]

if __name__ == '__main__':
    # Create a directory to hold the generated source code.
    OutputDirName = 'output'
    if not os.path.exists(OutputDirName):
        os.mkdir(OutputDirName)

    # Delete any stale files in the output directory.
    for fn in os.listdir(OutputDirName):
        fullname = os.path.join(OutputDirName, fn)
        print(fullname)
        os.remove(fullname)

    with open('words.txt', 'rt') as infile:
        text = infile.read()

    words = text.split()
    print('Read {} words, {} bytes.'.format(len(words), len(text)))

    for algorithm in AlgorithmList:
        name = algorithm.Name()
        sourceCode = algorithm.Compress(words)
        filename = os.path.join(OutputDirName, name + '.py')
        print('{:9d} {:s}'.format(len(sourceCode), filename))
        with open(filename, 'wt') as outfile:
            outfile.write(sourceCode)

    sys.exit(0)
