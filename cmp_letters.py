from huffman import HuffmanEncoder
from binary_tools import BitBuffer

class Compressor:
    r'''Strategy:
    Use Huffman encoding on the symbol set a-z and \n.
    '''
    def Name(self):
        return 'letters'

    def Compress(self, words):
        charRoot = self._HuffmanCode(words)
        charCode = charRoot.MakeEncoding()
        buf = self._Encode(words, charCode)
        source = "Char=" + charRoot.SourceCode() + "\n"
        source += "NumChars={:d}\n".format(sum(1+len(w) for w in words)-1)
        source += "Bits=r'''\n" + buf.Format() + "'''\n"
        return source

    def _Encode(self, words, charCode):
        buf = BitBuffer()
        for w in words:
            for c in w:
                buf.Append(charCode[c])
            buf.Append(charCode['\n'])
        return buf

    def _HuffmanCode(self, words):
        charHuff = HuffmanEncoder()
        for w in words:
            for c in w:
                charHuff.Tally(c)
            charHuff.Tally('\n')
        return charHuff.Compile()
