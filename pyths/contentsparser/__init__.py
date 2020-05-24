from .contentsparser import gen_program_record
from .datahandler import classify_by_channel, export


def main(htmldata, csvdata):
    with open(htmldata, 'r') as f:
        html_doc = f.read()
    records = gen_program_record(html_doc)
    program_list = classify_by_channel(records)
    export(program_list, outfile=csvdata)
