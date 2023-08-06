def by_mean(data_frame):
    df = data_frame[data_frame.dtypes[data_frame.dtypes != 'object'].index]
    null_values = df.isnull().sum()
    # replace null value with mean
    for (item, value) in null_values.items():
        if value > 0:
            data_frame[item] = data_frame[item].fillna(
                data_frame[item].mean())
    return data_frame


def by_mode(data_frame):
    df = data_frame[data_frame.dtypes[data_frame.dtypes != 'object'].index]
    null_values = df.isnull().sum()
    # replace null value with mean
    for (item, value) in null_values.items():
        if value > 0:
            data_frame[item] = data_frame[item].fillna(
                data_frame[item].mode()[0])
    return data_frame


def by_median(data_frame):
    df = data_frame[data_frame.dtypes[data_frame.dtypes != 'object'].index]
    null_values = df.isnull().sum()
    # replace null value with mean
    for (item, value) in null_values.items():
        if value > 0:
            data_frame[item] = data_frame[item].fillna(
                data_frame[item].median())
    return data_frame
