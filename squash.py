#!/usr/bin/env python3
import sys

if __name__ == '__main__':
    with open('words.txt', 'rt') as infile:
        words = infile.read().split()
        print('Read {} words'.format(len(words)))
    sys.exit(0)