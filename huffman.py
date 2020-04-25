#!/usr/bin/env python3
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

class HuffmanNode:
    def __init__(self, symbol, count, left, right):
        self.symbol = symbol
        self.count = count
        self.left = left
        self.right = right

    def __lt__(self, other):
        # Allows nodes to be sorted by count
        return self.count < other.count

    def MakeEncoding(self):
        return self._MakeEncoding({}, '')

    def _MakeEncoding(self, encoding, bitstring):
        # Recursively visit the tree to compute the bit string for each symbol.
        # The result is a dictionary such that encoding[symbol] = bitstring,
        # where bitstring is a string containing 0 and 1 characters like '10110100'.
        if self.symbol is not None:
            encoding[self.symbol] = bitstring
        if self.left is not None:
            self.left._MakeEncoding(encoding, bitstring + '0')
        if self.right is not None:
            self.right._MakeEncoding(encoding, bitstring + '1')
        return encoding

    def TreeTuple(self):
        # Convert the tree into a tuple format.
        # Each internal node becomes a tuple (left, right).
        # Each leaf node is just the symbol by itself.
        if self.symbol is not None:
            return self.symbol
        return (self.left.TreeTuple(), self.right.TreeTuple())

    def SourceCode(self):
        return repr(self.TreeTuple()).replace(' ', '')


class HuffmanEncoder:
    def __init__(self):
        self.table = {}

    def Tally(self, symbol):
        self.table[symbol] = 1 + self.table.get(symbol, 0)

    def Compile(self):
        if len(self.table) == 0:
            raise Exception('Huffman encoder needs to have at least one symbol.')

        # Build a binary tree that allows us to use a variable
        # number of bits to encode each symbol based on its probability.
        # Make a list of HuffmanNodes.
        # Keep it sorted in ascending order of frequency.
        tree = sorted(HuffmanNode(x[0], x[1], None, None) for x in self.table.items())

        # While there is more than one node at the top of the tree,
        # keep removing the least populated pair of items and combine
        # them into a new internal node.
        while len(tree) != 1:
            a, b, *rest = tree
            node = HuffmanNode(None, a.count + b.count, a, b)
            tree = sorted([node] + rest)

        # The single remaining node is the root node of the tree.
        return tree[0]
