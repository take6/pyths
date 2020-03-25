import os


def remove_file(path):
    if os.path.isdir(path):
        os.removedirs(path)
    else:
        os.remove(path)


def save_data(df, filename, overwrite=False):
    if os.path.exists(filename):
        if overwrite:
            remove_file(filename)
        else:
            print('ERROR: {} cannot overwrite'.format(filename))

    df.to_csv(filename, header=False, index=False)