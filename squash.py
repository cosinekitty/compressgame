#!/usr/bin/env python3
import sys
import os
import subprocess

CommonHeadCode = '#!/usr/bin/env python3\n'

CommonTailCode = r'''
if __name__ == "__main__":
    print(Expand())
'''

#--------------------------------------------------------------------

class Squash_PlainText:
    def Name(self):
        return 'plaintext'

    def Compress(self, words):
        return "r'''" + '\n'.join(words) + "'''\n"

#--------------------------------------------------------------------

class HuffmanNode:
    def __init__(self, symbol, count, left, right):
        self.symbol = symbol
        self.count = count
        self.left = left
        self.right = right

    def __lt__(self, other):
        # Allows nodes to be sorted by count
        return self.count < other.count

    def MakeEncoding(self, encoding, bitstring):
        if self.symbol is not None:
            encoding[self.symbol] = bitstring
        if self.left is not None:
            self.left.MakeEncoding(encoding, bitstring + '0')
        if self.right is not None:
            self.right.MakeEncoding(encoding, bitstring + '1')
        return encoding


class HuffmanEncoder:
    def __init__(self):
        self.table = {}

    def Tally(self, symbol):
        if symbol in self.table:
            self.table[symbol] += 1
        else:
            self.table[symbol] = 1

    def Compile(self):
        # Build a binary tree that allows us to use a variable
        # number of bits to encode each symbol based on its probability.
        # Make a list of HuffmanNodes.
        # Keep it sorted in ascending order of frequency.
        tree = sorted(HuffmanNode(x[0], x[1], None, None) for x in self.table.items())

        # While there is more than one node at the top of the tree,
        # keep removing the least populated pair of items and combine
        # them into a new internal node.
        while len(tree) > 1:
            a, b, *rest = tree
            node = HuffmanNode(None, a.count + b.count, a, b)
            tree = sorted([node] + rest)

        if len(tree) != 1:
            raise Exception('Huffman encoder has {} remaining nodes.'.format(len(tree)))

        # Recursively visit the tree to compute the bit string for each symbol.
        # The result is a dictionary such that encoding[symbol] = bitstring,
        # where bitstring is a string containing 0 and 1 characters like '10110100'.
        return tree[0].MakeEncoding({}, '')

#--------------------------------------------------------------------

class Squash_Huffman:
    r'''Strategy:
        1. Figure out how much each word has in common with the previous.
           For example, "apple" followed by "apples" has 5 letters in common.
           We can encode "apples" as (5, "s"), meaning, repeat 5 letters from
           the previous word, then append "s".
        2. Use Huffman encoding on the common-letter counts.
        3. Use Huffman encoding on the tail part of each word.
    '''
    def Name(self):
        return 'huffman'

    def Compress(self, words):
        repeatCode, tailCode, charCode = self._HuffmanCodes(words)
        pw = ''
        bits = ''
        for w in words:
            prefix = self._LettersInCommon(pw, w)
            bits += repeatCode[prefix]
            tail = len(w) - prefix
            bits += tailCode[tail]
            for c in w[prefix:]:
                bits += charCode[c]
            pw = w

        # Encode the 'bits' string, that contains a sequence of '0' and '1' chars,
        # into base64. Each base64 output character represents 6 bits, because 2**6 == 64.
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        text = ''
        lineLength = 0
        while len(bits) > 0:
            # If there are fewer than 6 bits remaining, pad with '0' on the end.
            while len(bits) < 6:
                bits += '0'
            # Remove the next 6 bits.
            chunk = bits[:6]
            bits = bits[6:]
            # Compute the integer index from 'chunk'
            index = 0
            for b in chunk:
                index <<= 1
                if b == '1':
                    index |= 1
            text += alphabet[index]
            lineLength += 1
            if lineLength == 80:
                text += '\n'
                lineLength = 0
        print(text)
        return "r'''\n" + text + "'''\n"

    def _HuffmanCodes(self, words):
        repeatHuff = HuffmanEncoder()
        tailHuff = HuffmanEncoder()
        charHuff = HuffmanEncoder()
        pw = ''
        for w in words:
            prefix = self._LettersInCommon(pw, w)
            repeatHuff.Tally(prefix)
            tailHuff.Tally(len(w) - prefix)
            for c in w[prefix:]:
                charHuff.Tally(c)
            pw = w
        return repeatHuff.Compile(), tailHuff.Compile(), charHuff.Compile()

    def _LettersInCommon(self, a, b):
        n = min(len(a), len(b))
        for i in range(n):
            if a[i] != b[i]:
                return i
        return n

#--------------------------------------------------------------------

AlgorithmList = [
    Squash_PlainText(),
    Squash_Huffman()
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
        compressedDataCode = 'Data = ' + algorithm.Compress(words)
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
