#!/usr/bin/env python
from optparse import OptionParser
from pyffmpeg import split_by_manifest, split_by_seconds


def main():
    parser = OptionParser()

    parser.add_option("-f", "--file",
                        dest = "filename",
                        help = "File to split, for example sample.avi",
                        type = "string",
                        action = "store"
                        )
    parser.add_option("-s", "--split-size",
                        dest = "split_size",
                        help = "Split or chunk size in seconds, for example 10",
                        type = "int",
                        action = "store"
                        )
    parser.add_option("-m", "--manifest",
                      dest = "manifest",
                      help = "Split video based on a json manifest file. ",
                      type = "string",
                      action = "store"
                     )
    parser.add_option("-v", "--vcodec",
                      dest = "vcodec",
                      help = "Video codec to use. ",
                      type = "string",
                      default = "copy",
                      action = "store"
                     )
    parser.add_option("-a", "--acodec",
                      dest = "acodec",
                      help = "Audio codec to use. ",
                      type = "string",
                      default = "copy",
                      action = "store"
                     )
    (options, args) = parser.parse_args()

    if options.filename and options.manifest:
        split_by_manifest(**(options.__dict__))
    elif options.filename and options.split_size:
        split_by_seconds(**(options.__dict__))
    else:
        parser.print_help()
        raise SystemExit

if __name__ == '__main__':
    main()
