from .contentsparser import gen_program_record
from .datahandler import classify_by_channel, export


###
def configure(parser):
    parser.add_argument(
        'htmldata',
        help='name of input HTML file name'
    )
    parser.add_argument(
        'csvdata',
        help='name of output CSV file name'
    )


def get_help():
    return 'parse TV program'


def main(args):
    htmldata = args.htmldata
    csvdata = args.csvdata

    status = 0
    try:
        with open(htmldata, 'r') as f:
            html_doc = f.read()
        records = gen_program_record(html_doc)
        program_list = classify_by_channel(records)
        export(program_list, outfile=csvdata)
    except Exception as e:
        print('ERROR: {}'.format(str(e)))
        status = 1

    return None, status
