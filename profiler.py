import argparse
import os
import sys

from modules.Core import ProfilerCore

PATH = os.path.dirname(os.path.abspath(__file__))


def workdir_path(input_data):
    if input_data.startswith('.'):
        return PATH + input_data[1:]
    elif input_data.startswith('/'):
        if os.path.isdir(input_data):
            return input_data
        else:
            os.makedirs(input_data, exist_ok=True)
    return input_data


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', dest='workdir', action='store',
                        type=workdir_path, default=PATH,
                        help='work directory path')
    parser.add_argument('-s', dest='sortby', action='store', default='time',
                        type=str,
                        help='chose sort by parameter (default: time)')
    parser.add_argument('-i', dest='interval', action='store', default=10,
                        type=int, help='chose interval in ms (default: 10ms)')
    parser.add_argument('program', action='store', type=str,
                        help='name for program e.g. hello.py')
    parser.add_argument('argv', action='store', nargs='*',
                        help='program arguments')
    return parser


def main():
    parser = get_arg_parser()
    args = parser.parse_args()
    if len(args.__dict__) > 0:
        program_name = args.program
        arguments = args.argv
        workdir = args.workdir
        sort_by = args.sortby
        interval = args.interval
        globs = {'__file__': program_name, '__name__': '__main__',
                 '__package__': None, '__cached__': None, }
        p = ProfilerCore(globs, arguments, workdir, sort_by, interval)
        p.start()
    else:
        parser.print_usage()
        sys.exit(2)


if __name__ == '__main__':
    main()
