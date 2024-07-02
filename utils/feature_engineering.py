import numpy as np


def generate_training_data(routes_df, encoded_types, sequence_length=10):
    X = []
    y = []

    # Combine numerical features and encoded types to ensure the correct input dimension
    feature_columns = ['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount'] + list(encoded_types.columns)

    for i in range(len(routes_df) - sequence_length):
        seq_X = routes_df.iloc[i:i + sequence_length][feature_columns]
        seq_y = routes_df.iloc[i + sequence_length][['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount']]

        X.append(seq_X.values)
        y.append(seq_y.values)

    X = np.array(X)
    y = np.array(y)

    return X, y

def prepare_prediction_data(df, scaler):
    df['durationMinutes'] = df['duration'].apply(lambda x: int(x.split()[0]) if 'min' in x else int(x.split()[0]) * 60)
    df[['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount']] = scaler.transform(
        df[['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount']])
    return df
