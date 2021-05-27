scan-tagger
===========

A helper script for applying metadata from [Exif Notes] to scans.

[Exif Notes]: https://play.google.com/store/apps/details?id=com.tommihirvonen.exifnotes&hl=en_US&gl=US

## Introduction

Exif Notes is a great way to track your film shots and apply that metadata to
the digitized files.  However, I always need to do some manipulation of the
scripts it produces before I can actually run them.  `scan-tagger` is a tool to
help automate those changes.

## Installation

    [$]> python3 -m pip install scan-tagger

## Usage

In its simplest form, you can just run `scan-tagger` against your Exif Notes
script and provide a starting filename:

    [$]> scan-tagger Arista.EDU\ ULTRA\ 100_ExifToolCmds.txt 000010460001.jpg

This will perform a few basic adjustments on the file, and then update the
filenames to `000010460001.jpg`, `000010460002.jpg`, etc.

For more advanced usage, pass the `-i` option to enter interactive mode.  This
provides a small line-by-line interface modelled after `git add -p` that allows
more control over the process.
