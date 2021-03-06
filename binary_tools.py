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
class BitBuffer:
    def __init__(self):
        self.buf = bytearray()
        self.accum = 0
        self.nbits = 0
        self.column = 0

    def Append(self, pattern):
        data, dbits = pattern
        while self.nbits + dbits >= 6:
            # We can emit a complete base64 character to represent a chunk of 6 bits.
            grab = 6 - self.nbits
            mask = (1 << grab) - 1
            self.accum = (self.accum << grab) | (mask & (data >> (dbits - grab)))
            dbits -= grab
            self.buf.append(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'[self.accum])
            self.accum = 0
            self.nbits = 0
            self.column += 1
            if self.column == 80:
                self.buf.append(ord('\n'))
                self.column = 0

        # Transfer any residual data bits into the accumulator.
        if dbits >= 0:
            mask = (1 << dbits) - 1
            self.accum = (self.accum << dbits) | (mask & data)
            self.nbits += dbits

    def Format(self):
        # Flush any remaining bits left in the accumulator.
        if self.nbits > 0:
            self.Append((0, (6 - self.nbits)))

        # Always end on a newline.
        if self.column > 0:
            self.buf.append(ord('\n'))
            self.column = 0

        # Convert the bytes to utf-8 text.
        return self.buf.decode('utf-8')
