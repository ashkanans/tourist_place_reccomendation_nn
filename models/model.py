from keras import Sequential
from keras.src.layers import LSTM, Dense, Dropout


def create_model(input_dim, num_features):
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(None, input_dim)))
    model.add(Dropout(0.2))
    model.add(Dense(num_features, activation='linear'))  # Output layer for numerical features with linear activation
    model.compile(optimizer='adam', loss='mean_squared_error')  # Use mean squared error for regression
    return model