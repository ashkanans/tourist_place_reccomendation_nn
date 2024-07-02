import numpy as np
import pandas as pd
import sqlite3

from keras.src.saving import load_model


def predict_path(start_id, end_id, time_span, scaler, encoded_types, model_path='models/models/tour_guide_model.h5'):
    model = load_model(model_path)

    conn = sqlite3.connect(
        'C:\\Program Files\\heroku\\bin\\artwalk-1\\backend\\database_config\\database_artwalk\\database.db')
    query = '''
        SELECT r.originId, r.destId, r.distanceMeters, r.duration, r.created_at, p.rating, p.userRatingCount, p.types
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

        df['durationMinutes'] = df['duration'].apply(lambda x:
                                                     int(x.split()[0]) if x and 'min' in x else (
                                                         int(x.split()[0]) * 60 if x else None))

        df = df.dropna(subset=['durationMinutes'])

        # Apply the same scaler to numerical features
        df[['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount']] = scaler.transform(
            df[['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount']])

        # Ensure all expected type columns are present
        type_columns = list(encoded_types.columns)
        for col in type_columns:
            if col not in df.columns:
                df[col] = 0

        # Prepare input data X with shape (1, None, number_of_features)
        feature_columns = ['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount'] + list(encoded_types.columns)
        X = np.array(df[feature_columns].values)
        X = np.expand_dims(X, axis=0)  # Add batch dimension
        X = np.swapaxes(X, 0, 1)  # Swap axis to (None, 1, number_of_features) assuming predicting for a single sequence

        # Predict probabilities
        pred_probs = model.predict(X)

        # Ensure dimensions match
        if len(pred_probs) != len(df):
            raise ValueError(f"Length of pred_probs ({len(pred_probs)}) does not match length of DataFrame ({len(df)})")

        # Define type importance scores (higher scores prioritize higher)
        type_importance = {
            'tourist_attraction': 2,
            'historical_landmark': 1,
            'landmark': 1,
            'museum': 1,
            'art_gallery': 0,
            'church': 0,
            'park': 0,
            'event_venue': 0,
            'movie_theater': 0,
            'library': 0,
            'market': 0,
            'gift_shop':0,
            'ice_cream_shop': 0,
            'italian_restaurant': 0,
            'mediterranean_restaurant': 0,
            'seafood_restaurant': 0,
            'restaurant': 0,
            'performing_arts_theater': 0,
            'clothing_store': 0,
            'store': 0,
            'zoo': 0,
            'dog_park': 0,
            'rv_park': 0,
            'default': 0,  # Default weight for types not specified
        }

        # Adjust predicted probabilities based on type importance
        weighted_probs = []
        for index in range(len(df)):
            row = df.iloc[index]
            types = row.get('types', '').split(', ') if 'types' in row else []
            type_score = max(type_importance.get(t, 1.0) for t in types)
            weighted_prob = pred_probs[index] * type_score  # Adjusted calculation
            weighted_probs.append(weighted_prob.flatten().tolist()[0])

        # Assign weighted probabilities to DataFrame
        df['weighted_prob'] = weighted_probs

        # Sort by weighted probabilities descending to prioritize higher-scoring types
        df = df.sort_values(by='weighted_prob', ascending=False)

        # Find the next best location that is not already in path
        next_location = None
        for index, row in df.iterrows():
            if row['destId'] not in path:
                next_location = row
                break

        if next_location is None:
            break  # If no valid next location found, break out of the loop

        # Add next_location to path
        path.append(next_location['destId'])
        current_time += int(next_location['duration'])

        # Update the origin for the next prediction
        start_id = next_location['destId']

    conn.close()
    return path