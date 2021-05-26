#!/usr/bin/env python3

import argparse
import os
import stat
import sys

class ScanTaggerException(Exception):
    '''Class for any errors that should terminate the program and be passed on
    to the user.'''
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('pattern')
    args = parser.parse_args()

    counter, image_format_string = parse_image_pattern(args.pattern)

    # Add the executable bit.
    os.chmod(args.file, os.stat(args.file).st_mode | stat.S_IEXEC)

    # Store all our changes in memory.  This is easier than making changes
    # in-place, and the files are tiny so memory use isn't a concern.
    new_file = [
        '#!/bin/bash',
        'set -euo pipefail', # Bash "strict mode"
        '',
    ]

    with open(args.file, 'r') as f:
        for line in f:
            line = line.rstrip()
            # Continue on past blank lines.
            if not line:
                new_file.append(line)
                continue

            # Replace the filename of the image that we're tagging with the
            # actual filename we want to use.
            words = line.split()
            image_name = image_format_string % counter
            words[-1] = image_name
            new_file.append(' '.join(words))
            counter += 1

    with open(args.file, 'w') as f:
        for line in new_file:
            f.write(line)
            f.write('\n')

def parse_image_pattern(pattern):
    '''Split apart a filename into pieces we can increment.

    Args:
        pattern -- a numerical filename, e.g. '000010460001.jpg'

    Returns a tuple (counter, format_string):
        counter -- an integer derviced from the numerical part of the pattern
        format_string -- a Python format string that the counter can be pushed
            into to create a filename in the same pattern as the original.
    '''
    filename, extension = os.path.splitext(pattern)
    try:
        counter = int(filename)
    except ValueError:
        raise ScanTaggerException('%s is not a valid filename pattern.' % filename)

    length = len(filename)
    format_string = '%0' + str(length) + 'd' + extension

    return (counter, format_string)

if __name__ == '__main__':
    try:
        main()
    except ScanTaggerException as e:
        print(e)
        sys.exit(1)
