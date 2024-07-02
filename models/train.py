from models.model import create_model
from utils.data_processing import preprocess_data, load_data
from utils.feature_engineering import generate_training_data


def main():
    # Load and preprocess data
    routes_df, places_df = load_data('C:\\Program Files\\heroku\\bin\\artwalk-1\\backend\\database_config\\database_artwalk\\database.db')
    routes_df, scaler, encoded_types = preprocess_data(routes_df, places_df)

    # Select top 100,000 rows with highest rating and userRatingCount
    routes_df = routes_df.nlargest(100000, ['rating', 'userRatingCount'])

    # Generate training data
    X, y = generate_training_data(routes_df, encoded_types, sequence_length=10)

    # Create and train model
    input_dim = X.shape[2]  # Ensure input_dim matches the number of features
    num_features = y.shape[1]  # Assuming y is a 2D array with shape (num_samples, num_features)
    model = create_model(input_dim, num_features)
    model.fit(X, y, epochs=50, batch_size=64, validation_split=0.2)

    # Save the trained model
    model.save('models/tour_guide_model.h5')

if __name__ == "__main__":
    main()
