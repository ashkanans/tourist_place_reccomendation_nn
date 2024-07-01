import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from keras.models import load_model
from utils.data_processing import load_data, preprocess_data
from utils.feature_engineering import generate_training_data
from models.model import create_model

# Load and preprocess data
routes_df, places_df = load_data('tour_guide.db')
routes_df, scaler = preprocess_data(routes_df)

# Generate training data
X, y = generate_training_data(routes_df)

# Create and train model
input_dim = X.shape[2]
model = create_model(input_dim)
model.fit(X, y, epochs=10, batch_size=64, validation_split=0.2)

# Save the trained model
model.save('models/tour_guide_model.h5')
