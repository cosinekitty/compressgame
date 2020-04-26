#!/usr/bin/env python3
#
#   https://github.com/cosinekitty/compressgame
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
import base64

class BitBuffer:
    def __init__(self):
        self.buf = bytearray()
        self.accum = 0
        self.nbits = 0

    def Append(self, text):
        for c in text:
            self.accum = (self.accum << 1) | '01'.index(c)
            self.nbits += 1
            if self.nbits == 8:
                self.buf.append(self.accum)
                self.accum = 0
                self.nbits = 0

    def Format(self):
        # Flush any remaining bits left in the accumulator.
        if self.nbits > 0:
            self.Append('0' * (8 - self.nbits))

        # Convert to base64 encoding.
        text = base64.b64encode(self.buf).decode()

        # Add line breaks every 80 characters.
        width = 80
        pos = 0
        size = len(text)
        output = ''
        while pos < size:
            if size - pos > width:
                line = text[pos:pos+width]
            else:
                line = text[pos:]
            output += line + '\n'
            pos += len(line)

        return output
