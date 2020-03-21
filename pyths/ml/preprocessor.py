def drop_short_programs(df, threshold):
    # threshold in minutes
    subset = df[df['Duration'] > threshold]

    return subset


def drop_duplicate_rows(df, target=None):
    if target is None:
        # drop complete duplicates
        is_duplicate = df.duplicated(keep='first')
    elif isinstance(target, str):
        is_duplicate = df[target].duplicated(keep='first')
    else:
        raise RuntimeError('target {} is invalid.'.format(target))

    return df[~is_duplicate]


def preprocess(df):
    # only take programs with duration > 30min
    no_short = drop_short_programs(df, threshold=30)

    # drop rows with duplicate title
    no_dup = drop_duplicate_rows(no_short, target='Title')

    return no_dup
