import argparse

from . import informer
from . import contentsparser
from . import contentsreader
from . import ml


SUBCOMMANDS = {
    'get': contentsreader,
    'parse': contentsparser,
    'categorize': ml,
    'report': informer,
}


# factory for subcommand invocation
def invoke_subcommand(args):
    module = SUBCOMMANDS[args.subcommand]
    return module.main(args)


# main
def main():
    parser = argparse.ArgumentParser()

    # subparsers
    subparsers = parser.add_subparsers(dest='subcommand')
    for subcommand, module in SUBCOMMANDS.items():
        subparser = subparsers.add_parser(
            subcommand,
            help=module.get_help())
        module.configure(subparser)

    # parse args and invoke subcommand
    args = parser.parse_args()
    ret = invoke_subcommand(args)

    #if ret is not None:
    #    print(f'subcommand returned {ret}')


# execute main function
main()
