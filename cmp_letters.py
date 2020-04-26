from huffman import HuffmanEncoder
from binary_tools import Base64

class Compressor:
    r'''Strategy:
    Use Huffman encoding on the symbol set a-z and \n.
    '''
    def Name(self):
        return 'letters'

    def Compress(self, words):
        charRoot = self._HuffmanCode(words)
        charCode = charRoot.MakeEncoding()
        bits = self._Encode(words, charCode)
        source = "Char=" + charRoot.SourceCode() + "\n"
        source += "NumChars={:d}\n".format(sum(1+len(w) for w in words)-1)
        source += "Bits=r'''\n" + Base64(bits) + "'''\n"
        return source

    def _Encode(self, words, charCode):
        bits = ''
        for w in words:
            bits += ''.join(charCode[c] for c in w) + charCode['\n']
        return bits

    def _HuffmanCode(self, words):
        charHuff = HuffmanEncoder()
        for w in words:
            for c in w:
                charHuff.Tally(c)
            charHuff.Tally('\n')
        return charHuff.Compile()
