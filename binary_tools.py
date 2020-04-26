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

def Base64(bits):
    # Encode the 'bits' string, that contains a sequence of '0' and '1' chars,
    # into base64. Each base64 output character represents 6 bits, because 2**6 == 64.
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    text = ''
    lineLength = 0
    pos = 0
    nbits = len(bits)
    while pos < nbits:
        # Remove the next 6 bits.
        # If there are fewer than 6 bits remaining, pad with '0' on the end.
        if pos + 6 > nbits:
            chunk = bits[pos:]
            while len(chunk) < 6:
                chunk += '0'
        else:
            chunk = bits[pos:6+pos]
        pos += 6
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
    return text
