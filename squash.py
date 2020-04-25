#!/usr/bin/env python3
#
#    https://github.com/cosinekitty/compressgame
#
#    MIT License
#
#    Copyright (c) 2020 Don Cross <cosinekitty@gmail.com>
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.
#
import sys
import os
import subprocess
import cmp_letters
import cmp_prefix

CommonHeadCode = '#!/usr/bin/env python3\n'

CommonTailCode = r'''
if __name__ == "__main__":
    print(Expand())
'''

#--------------------------------------------------------------------

AlgorithmList = [
    cmp_letters.Compressor(),
    cmp_prefix.Compressor()
]

#--------------------------------------------------------------------

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
        compressedDataCode = algorithm.Compress(words)
        stubFileName = os.path.join(StubDirName, algorithm.Name() + '.py')
        with open(stubFileName, 'rt') as infile:
            stubCode = infile.read()
        targetFileName = os.path.join(OutputDirName, algorithm.Name() + '.py')
        code = CommonHeadCode + compressedDataCode + stubCode + CommonTailCode
        with open(targetFileName, 'wt') as outfile:
            outfile.write(code)
        print('{:9d} {:s}'.format(len(code), targetFileName))
        result = subprocess.run([sys.executable, targetFileName], check=True, stdout=subprocess.PIPE)
        check = result.stdout.decode('utf-8')
        if check != text:
            print('FAILURE: Generated text does not match original.')
            sys.exit(1)

    sys.exit(0)
