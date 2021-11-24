#!/usr/bin/env python3
"""A binary file viewer in the style of xxd with shift_jis text encoding.

xjis.py will render 3 columns:
- Offset
- Raw byte values
- Text display

The offsets are given as decimal numbers (but you can switch this to use
hexadecimal, if you prefer).

The raw byte values are given as hexadecimal values separated by spaces.

The text display will attempt to decode each 2-byte sequence as a Shift JIS
character.  If the result is a printable character, it will be displayed in the
third column.  Otherwise, a period (.) character will be shown to indicate each
non-printable byte.

Because a 2-byte Shift JIS character can start on the last byte of a line, some
lines in the text display will be longer than others, despite always showing
the same number of bytes per line in the raw byte column.
"""
import argparse
import sys
import unicodedata


ENC = 'shift_jis'
LINE_LEN = 16


def print_line(offset, line_bytes, line_chars, outstream, hex_style=False):
    sep = ' │ '
    bytevals = ' '.join([f'{x:02x}' for x in line_bytes])
    template = '{:6' + ('x' if hex_style else 'd') + '}'
    offlabel = template.format(offset)
    line = offlabel + sep + bytevals + sep + ''.join(line_chars)
    outstream.write(line + '\n')


def display(instream, outstream, hex_style=False):
    data = instream.read()
    i = 0
    offset = 0
    line_bytes = []
    line_chars = []
    next_byte = None
    while i < len(data):
        try:
            chars = data[i:i+2].decode(ENC)
            for ch in chars:
                if unicodedata.category(ch)[0] == 'C':
                    ch = '.'
                line_chars.append(ch)
            line_bytes.append(data[i])
            if len(line_bytes) < LINE_LEN:
                line_bytes.append(data[i+1])
            else:
                next_byte = data[i+1]
            i += 2
        except UnicodeDecodeError:
            line_chars.append('.')
            line_bytes.append(data[i])
            i += 1
        if len(line_bytes) >= LINE_LEN:
            print_line(offset, line_bytes, line_chars, outstream, hex_style)
            line_bytes = []
            line_chars = []
            if next_byte:
                line_bytes.append(next_byte)
                next_byte = None
            offset += LINE_LEN
    if line_bytes:
        print_line(line_bytes, line_chars, outstream)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--hex-style', action='store_true')
    parser.add_argument('filepath', nargs='?')

    args = parser.parse_args()
    if args.filepath and args.filepath != '-':
        with open(args.filepath, 'rb') as fp:
            display(fp, sys.stdout, args.hex_style)
    else:
        display(sys.stdin.buffer, sys.stdout, args.hex_style)
    sys.exit(0)
