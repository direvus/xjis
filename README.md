# xjis

A binary file viewer in the style of `xxd`, for Shift JIS text.

**xjis** is a command-line application to help you view binary data that
contains Shift JIS text.  Given a file or stream of bytes, xjis will display information in three columns:

- Offset
- Raw byte values
- Text display

The offsets are given as decimal numbers (but you can switch this to use
hexadecimal, if you prefer), counting from zero.

The raw byte values are given as hexadecimal values separated by spaces.

The text display will attempt to decode each 2-byte sequence as a Shift JIS
character.  If the result is a printable character, it will be displayed in the
third column.  Otherwise, a period (.) character will be shown to indicate each
non-printable byte.

Because a 2-byte Shift JIS character can start on the last byte of a line, some
lines in the text display will be longer than others, despite always showing
the same number of bytes per line in the raw byte column.

## Requirements

- Python 3.7+. xjis uses built-in libraries only, no package dependencies.
- A unicode-capable terminal.

## Installation

Download xjis.py on to your computer and execute it.

## Invocation

```
xjis.py [-H] [path]
```

### Options

- *-H / --hex-style*: Select hexadecimal byte offsets in the first display
  column.  If you do not specify this option, the byte offsets are shown in
  decimal.

### Positional arguments

- *path*: A path to the file you want to view.  If you do not specify a path,
  or the path is `-`, xjis.py will expect to receive binary data on stdin.
