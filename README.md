

# Tour Guide App

The Tour Guide App recommends touristic paths between locations based on walking distances and times, considering user-specified time constraints and prioritizing locations with high ratings and user rating counts.

## Project Structure

```
tour_guide_app/
│
├── data/                   # Directory for datasets
│   ├── locations.csv       # Dataset containing touristic locations and walking times
│   ├── processed_data.pkl  # Preprocessed data (optional)
│
├── models/                 # Directory for model-related scripts
│   ├── model.py            # Neural network model definition
│   ├── train.py            # Script for training the model
│   ├── predict.py          # Script for making predictions
│
├── notebooks/              # Jupyter notebooks for data exploration and model training
│   ├── data_exploration.ipynb  # Notebook for exploring the dataset
│   ├── model_training.ipynb    # Notebook for training the model
│
├── utils/                  # Directory for utility functions
│   ├── data_processing.py  # Functions for data loading and preprocessing
│   ├── feature_engineering.py # Functions for feature engineering
│
├── main.py                 # Main entry point of the application
├── requirements.txt        # List of Python dependencies
├── README.md               # Project documentation (this file)
├── .gitignore              # Git ignore file
```

## Getting Started

### Prerequisites

- Python 3.x
- Install dependencies using `pip`:

  ```bash
  pip install -r requirements.txt
  ```

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd tour_guide_app
   ```

2. **Setup SQLite Database:**

   - Create a SQLite database (`tour_guide.db`) and execute the SQL commands to create `routes` and `places` tables as described earlier.

3. **Train the Model:**

   - Train the neural network model to predict touristic paths. Run:

     ```bash
     python models/train.py
     ```

4. **Run the Application:**

   - Start the application to recommend touristic paths based on user input. Run:

     ```bash
     python main.py
     ```

## Usage

- When prompted, enter the starting location ID, ending location ID, and the desired time span in minutes.
- The application will generate and recommend a path of touristic locations based on the trained model's predictions.

## Features

- **Data Preprocessing:** Convert durations to minutes and normalize features for model training.
- **Model Training:** Utilize an LSTM neural network to learn and predict touristic paths.
- **Path Recommendation:** Prioritize locations with high ratings and user rating counts within the specified time constraints.

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or feature requests, please open an issue or a pull request.

## License


## Acknowledgments

