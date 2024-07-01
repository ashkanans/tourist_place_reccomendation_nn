import sqlite3
import pandas as pd
import numpy as np
from keras.src.saving import load_model

from utils.data_processing import load_data, preprocess_data
from utils.feature_engineering import prepare_prediction_data


def predict_path(start_id, end_id, time_span, scaler, model_path='models/tour_guide_model.h5'):
    model = load_model(model_path)

    conn = sqlite3.connect('tour_guide.db')
    query = '''
    SELECT r.originId, r.destId, r.distanceMeters, r.duration, r.created_at, p.rating, p.userRatingCount
    FROM routes r
    JOIN places p ON r.destId = p.id
    WHERE r.originId = ?
    '''

    path = [start_id]
    current_time = 0

    while current_time < time_span:
        df = pd.read_sql(query, conn, params=(start_id,))
        if df.empty:
            break
        df['durationMinutes'] = df['duration'].apply(
            lambda x: int(x.split()[0]) if 'min' in x else int(x.split()[0]) * 60)
        df[['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount']] = scaler.transform(
            df[['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount']])

        X = np.array([df[['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount']].values])
        pred_probs = model.predict(X)[0]

        # Filter predictions for locations within the remaining time
        df['pred_prob'] = pred_probs
        df = df[df['durationMinutes'] + current_time < time_span]
        df = df.sort_values(by=['rating', 'userRatingCount', 'pred_prob'], ascending=False)

        if df.empty:
            break

        next_location = df.iloc[0]
        path.append(next_location['destId'])
        current_time += next_location['durationMinutes']

        # Update the origin for the next prediction
        start_id = next_location['destId']

    conn.close()
    return path
