from pathlib import Path
from re import compile
from sys import stdin
from textwrap import indent
from .argparser import ArgParser


class Main(object):
    @classmethod
    def entrypoint(cls):
        cls().main()

    def __init__(self):
        self.args, unknown = parser.parse_known_args()
        self.xargs = xargs_parse(unknown)

    def main(self):
        lines = stdin.read().splitlines()
        for src, dst in self.xargs.items():
            lines = self.replace(lines, src, dst)
        for line in lines:
            print(line)

    def replace(self, lines, src, dst):
        for line in lines:
            d = dst
            if '\n' in d:
                i = len(head_spaces.match(line).group(0))
                d = indent(d, ' ' * i).strip()
            yield line.replace(src, d)


def xargs_parse(args):
    xargs = {}
    for arg in args:
        if match := xargs_format.match(arg):
            src, dst = match.groups()
            xargs[src] = xargs_expand(dst)
        else:
            raise Exception(f'Invalid xarg "{arg}"')
    return xargs


def xargs_expand(val):
    if match := xargs_file_format.match(val):
        return Path(match.group(1)).read_text()
    else:
        return val


parser = ArgParser()

xargs_format = compile(r'^(.+?)=(.*)$')

xargs_file_format = compile(r'^@(.+)$')

head_spaces = compile(r'^\s*')
