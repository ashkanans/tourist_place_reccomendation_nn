from models.predict import predict_path
from utils.data_processing import load_data, preprocess_data


def main():
    start_id = input("Enter starting location ID: ")
    end_id = input("Enter ending location ID: ")
    time_span = int(input("Enter time span in minutes: "))

    routes_df, places_df = load_data('tour_guide.db')
    _, scaler = preprocess_data(routes_df)

    recommended_path = predict_path(start_id, end_id, time_span, scaler)
    print("Recommended path:", recommended_path)


if __name__ == "__main__":
    main()
