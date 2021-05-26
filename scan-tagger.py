#!/usr/bin/env python3

import argparse
import os
import stat

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('pattern')
    args = parser.parse_args()

    # Add the executable bit.
    os.chmod(args.file, os.stat(args.file).st_mode | stat.S_IEXEC)

    # Store all our changes in memory.  This is easier than making changes
    # in-place, and the files are tiny so memory use isn't a concern.
    new_file = [
        '#!/bin/bash',
        'set -euo pipefail', # Bash "strict mode"
        '',
    ]

    counter = 1
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
            image_name = '%s%02d.jpg' % (args.pattern, counter)
            words[-1] = image_name
            new_file.append(' '.join(words))
            counter += 1

    with open(args.file, 'w') as f:
        for line in new_file:
            f.write(line)
            f.write('\n')

if __name__ == '__main__':
    main()
