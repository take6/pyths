from .exporter import save_data
from .loader import load_data, load_model
from .preprocessor import preprocess

from .naivebayes import NaiveBayes


###
def configure(parser):
    parser.add_argument(
        'csvdata',
        help='name of input CSV file name'
    )
    parser.add_argument(
        'modeldata',
        help='model data for categorization'
    )


def get_help():
    return 'categorize TV programs'


def main(args):
    csvdata = args.csvdata
    modeldata = args.modeldata

    status = 0
    try:
        df = load_data(csvdata)
        machine = load_model(modeldata)
        categorized = machine.categorize(df)
        save_data(categorized, csvdata, overwrite=True)
    except Exception as e:
        print('ERROR: {}'.format(str(e)))
        status = 1

    return None, status
