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
