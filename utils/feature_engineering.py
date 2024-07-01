import numpy as np
import pandas as pd


def generate_training_data(routes_df):
    sequences = []
    next_destinations = []

    for origin in routes_df['originId'].unique():
        subset = routes_df[routes_df['originId'] == origin]
        if len(subset) < 2:
            continue

        for i in range(len(subset) - 1):
            seq = subset.iloc[:i + 1][['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount']].values
            next_dest = subset.iloc[i + 1]['destId']
            sequences.append(seq)
            next_destinations.append(next_dest)

    X = np.array([np.pad(seq, ((0, 10 - len(seq)), (0, 0)), 'constant') for seq in sequences])
    y = pd.Series(next_destinations).astype('category').cat.codes.values

    return X, y


def prepare_prediction_data(df, scaler):
    df['durationMinutes'] = df['duration'].apply(lambda x: int(x.split()[0]) if 'min' in x else int(x.split()[0]) * 60)
    df[['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount']] = scaler.transform(
        df[['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount']])
    return df
