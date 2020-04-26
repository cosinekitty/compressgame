from huffman import HuffmanEncoder
from binary_tools import BitBuffer

class Compressor:
    r'''This one is similar to cmp_prefix.py, only we
    tally separate counters for each possible previous letter.
    Some letters are more likely to follow than others.
    For example, t often comes right before e or h.
    '''
    def Name(self):
        return 'pairs'

    def Compress(self, words):
        repeatRoot, tailRoot, charRootTable = self._HuffmanCodes(words)
        repeatCode = repeatRoot.MakeEncoding()
        tailCode = tailRoot.MakeEncoding()
        charCodeTable = [r.MakeEncoding() for r in charRootTable]
        buf = self._Encode(words, repeatCode, tailCode, charCodeTable)
        source = "Repeat=" + repeatRoot.SourceCode() + "\n"
        source += "Tail=" + tailRoot.SourceCode() + "\n"
        source += "Char=[" + ",\n".join(r.SourceCode() for r in charRootTable) + "]\n"
        source += "NumWords={:d}\n".format(len(words))
        source += "Bits=r'''\n" + buf.Format() + "'''\n"
        return source

    def _Encode(self, words, repeatCode, tailCode, charCodeTable):
        pw = ''
        buf = BitBuffer()
        for w in words:
            prefix = self._LettersInCommon(pw, w)
            buf.Append(repeatCode[prefix])
            tail = w[prefix:]
            buf.Append(tailCode[len(tail)])
            if prefix == 0:
                i = 0
            else:
                i = ord(w[prefix-1]) - ord('`')
            for c in tail:
                buf.Append(charCodeTable[i][c])
                i = ord(c) - ord('`')
            pw = w
        return buf

    def _HuffmanCodes(self, words):
        repeatHuff = HuffmanEncoder()
        tailHuff = HuffmanEncoder()
        charHuffTable = [HuffmanEncoder() for _ in range(27)]
        pw = ''
        for w in words:
            prefix = self._LettersInCommon(pw, w)
            repeatHuff.Tally(prefix)
            tailHuff.Tally(len(w) - prefix)
            if prefix == 0:
                # Use index 0 to represent that there is no previous character.
                i = 0
            else:
                # We take advantage of the fact that the backquote character '``
                # comes right before 'a' in the ASCII table.
                i = ord(w[prefix-1]) - ord('`')

            for c in w[prefix:]:
                charHuffTable[i].Tally(c)
                i = ord(c) - ord('`')

            pw = w

        charRootTable = [h.Compile() for h in charHuffTable]
        return repeatHuff.Compile(), tailHuff.Compile(), charRootTable

    def _LettersInCommon(self, a, b):
        n = min(len(a), len(b))
        for i in range(n):
            if a[i] != b[i]:
                return i
        return n

