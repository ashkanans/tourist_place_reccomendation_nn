from keras import Sequential
from keras.src.layers import LSTM, Dense


def create_model(input_dim):
    model = Sequential()
    model.add(LSTM(128, input_shape=(None, input_dim), return_sequences=True))
    model.add(LSTM(128))
    model.add(Dense(700, activation='softmax'))  # Output layer representing 700 possible locations
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model
