import sqlite3
import pandas as pd


def load_data(database_path):
    conn = sqlite3.connect(database_path)

    # Load routes data
    routes_query = '''
    SELECT r.originId, r.destId, r.distanceMeters, r.duration, r.created_at, p.rating, p.userRatingCount
    FROM routes r
    JOIN places p ON r.destId = p.id
    '''
    routes_df = pd.read_sql(routes_query, conn)

    # Load places data
    places_query = 'SELECT * FROM places'
    places_df = pd.read_sql(places_query, conn)

    conn.close()

    return routes_df, places_df


def preprocess_data(routes_df):
    # Convert duration to minutes
    routes_df['durationMinutes'] = routes_df['duration'].apply(
        lambda x: int(x.split()[0]) if 'min' in x else int(x.split()[0]) * 60)

    # Normalize features
    scaler = StandardScaler()
    features = ['distanceMeters', 'durationMinutes', 'rating', 'userRatingCount']
    routes_df[features] = scaler.fit_transform(routes_df[features])

    return routes_df, scaler
