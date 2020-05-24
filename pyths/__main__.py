import argparse

from . import informer
from . import contentsparser
from . import contentsreader
from . import ml


#
# SUBCOMMAND FUNCTIONS
#
# subcommand functions must accept one argument named 'args'
# which is returned by ArgumentParser.
#
# name of subcommand functions must match one of the subcommand
# registered to the ArgumentParser
#
def get(args):
    datestring = args.yyyymmdd
    htmldata = args.htmldata
    contentsreader.main(htmldata=htmldata, datestr=datestring)


def parse(args):
    htmldata = args.htmldata
    csvdata = args.csvdata
    contentsparser.main(htmldata=htmldata, csvdata=csvdata)


def categorize(args):
    csvdata = args.csvdata
    modeldata = args.modeldata
    ml.main(csvdata=csvdata, modeldata=modeldata)


def report(args):
    csvdata = args.csvdata
    informer.main(csvdata)


# factory for subcommand invocation
def invoke_subcommand(args):
    return globals()[args.subcommand](args)


# helper for subcommand configuration
def configure_get(subparsers):
    parser = subparsers.add_parser(
        'get',
        help='get TV program data as HTML')
    parser.add_argument(
        'yyyymmdd',
        help='date for TV program to get')
    parser.add_argument(
        'htmldata',
        help='name of output HTML file name')


def configure_parse(subparsers):
    parser = subparsers.add_parser(
        'parse',
        help='parse TV program'
    )
    parser.add_argument(
        'htmldata',
        help='name of input HTML file name'
    )
    parser.add_argument(
        'csvdata',
        help='name of output CSV file name'
    )


def configure_categorize(subparsers):
    parser = subparsers.add_parser(
        'categorize',
        help='categorize TV programs'
    )
    parser.add_argument(
        'csvdata',
        help='name of input CSV file name'
    )
    parser.add_argument(
        'modeldata',
        help='model data for categorization'
    )


def configure_report(subparsers):
    parser = subparsers.add_parser(
        'report',
        help='report 2H suspense drama')
    parser.add_argument(
        'csvdata',
        help='name of CSV file')


# main
def main():
    parser = argparse.ArgumentParser()

    # subparsers
    subparsers = parser.add_subparsers(dest='subcommand')

    # get subcommand
    configure_get(subparsers)

    # parse subcommand
    configure_parse(subparsers)

    # categorize subcommand
    configure_categorize(subparsers)

    # report subcommand
    configure_report(subparsers)

    # parse args and invoke subcommand
    args = parser.parse_args()
    ret = invoke_subcommand(args)

    if ret is not None:
        print(f'subcommand returned {ret}')


# execute main function
main()
