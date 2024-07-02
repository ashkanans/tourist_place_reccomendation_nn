from models.predict import predict_path
from utils.data_processing import load_data, preprocess_data


from utils.data_processing import load_data, preprocess_data

def main():
    start_id = "ChIJ1UCDJ1NgLxMRtrsCzOHxdvY"
    end_id = "ChIJKcGbg2NgLxMRthZkUqDs4M8"
    time_span = 120 * 60

    routes_df, places_df = load_data('C:\\Program Files\\heroku\\bin\\artwalk-1\\backend\\database_config\\database_artwalk\\database.db')
    routes_df, scaler, encoded_types = preprocess_data(routes_df, places_df)  # Ensure to also get encoded_types from preprocess_data

    # Select top 100,000 rows with highest rating and userRatingCount
    routes_df = routes_df.nlargest(100000, ['rating', 'userRatingCount'])

    recommended_path = predict_path(start_id, end_id, time_span, scaler, encoded_types)  # Pass encoded_types to predict_path
    print("Recommended path:", recommended_path)

if __name__ == "__main__":
    main()
