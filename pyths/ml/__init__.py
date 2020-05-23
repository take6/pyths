from .exporter import save_data
from .loader import load_data, load_model
from .preprocessor import preprocess

from .naivebayes import NaiveBayes


def main(csvdata, modeldata):
    df = load_data(csvdata)
    machine = load_model(modeldata)
    categorized = machine.categorize(df)
    save_data(categorized, csvdata, overwrite=True)
