#!/usr/bin/env python3

import argparse
import os
import platform
import stat
import subprocess
import sys
import tempfile

class ScanTaggerException(Exception):
    '''Class for any errors that should terminate the program and be passed on
    to the user.'''
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interactive', action='store_true')
    parser.add_argument('--keep-backups', action='store_true')
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
            if not args.keep_backups:
                # Put this argument at the beginning so it doesn't mess with
                # our manipulations of the filename when duplicating lines.
                words.insert(1, '-overwrite_original')
            new_lines = [' '.join(words)]

            if args.interactive:
                while True:
                    print('-' + line)
                    for new_line in new_lines:
                        print('+' + new_line)
                    choice = input('Continue with this change? [y,q,a,e,d,o,?] ')
                    if choice == 'y':
                        print()
                        break
                    elif choice == 'q':
                        sys.exit(1)
                    elif choice == 'a':
                        args.interactive = False
                        break
                    elif choice == 'e':
                        with tempfile.NamedTemporaryFile(mode='w',
                                                         delete=False) as scratch:
                            scratch.write('\n'.join(new_lines))
                            tempfile_name = scratch.name
                            # Close the file so we can manipulate it in a text
                            # editor.
                        # Open file in the user's preferred editor; if they
                        # don't specify, assume vi is available thanks to the
                        # Single UNIX Specification.
                        editor = os.getenv('EDITOR', 'vi')
                        subprocess.run([editor, tempfile_name])
                        with open(tempfile_name, 'r') as scratch:
                            new_lines = scratch.readlines()
                    elif choice == 'd':
                        counter += 1
                        image_name = image_format_string % counter
                        words[-1] = image_name
                        new_lines.append(' '.join(words))
                    elif choice == 'o':
                        image_name = image_format_string % counter
                        # Open the default handler for this file.
                        # https://stackoverflow.com/q/434597/120999
                        if platform.system() == 'Darwin':
                            subprocess.run(['open', image_name])
                        elif platform.system() == 'Linux':
                            subprocess.run(['xdg-open', image_name])
                        elif platform.system() == 'Windows':
                            subprocess.run(['start', image_name], shell=True)
                        else:
                            print("Unknown operating system.")
                    # We intentionally don't check for '?', as it has the same
                    # behavior as any unknown input.
                    else:
                        print("y - keep this change as-is")
                        print("q - quit the program")
                        print("a - keep this change and answer y to all subsequent changes")
                        print("e - manually edit the line")
                        print("d - duplicate line (useful for unrecorded shots at the beginning of a roll)")
                        print("o - open the image for viewing")
                        print("? - print help")
                    print()

            new_file.extend(new_lines)
            counter += 1

    with open(args.file, 'w') as f:
        for line in new_file:
            f.write(line)
            f.write('\n')

    subprocess.run(['./' + args.file], check=True)

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
