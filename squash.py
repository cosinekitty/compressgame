#!/usr/bin/env python3
import sys
import os

CommonHeadCode = '#!/usr/bin/env python3\n'

CommonTailCode = r'''
if __name__ == "__main__":
    print(Expand())
'''

class Squash_PlainText:
    def Name(self):
        return 'plaintext'

    def Compress(self, words):
        return "r'''" + '\n'.join(words) + "'''\n"

AlgorithmList = [
    Squash_PlainText()
]

if __name__ == '__main__':
    StubDirName = 'stubs'

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
        compressedDataCode = 'Data = ' + algorithm.Compress(words)
        stubFileName = os.path.join(StubDirName, algorithm.Name() + '.py')
        with open(stubFileName, 'rt') as infile:
            stubCode = infile.read()
        targetFileName = os.path.join(OutputDirName, algorithm.Name() + '.py')
        code = CommonHeadCode + compressedDataCode + stubCode + CommonTailCode
        with open(targetFileName, 'wt') as outfile:
            outfile.write(code)
        print('{:9d} {:s}'.format(len(code), targetFileName))

    sys.exit(0)
