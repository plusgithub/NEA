import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, MaxPooling2D, Bidirectional, Reshape, BatchNormalization, Convolution2D, Flatten, Dense
from tensorflow.keras.initializers import TruncatedNormal

def create_model():
    model = Sequential()

    model.add(Convolution2D(input_shape=[40,32,1], filters=64, kernel_size=[20, 8], strides=[1, 1], padding='same', kernel_initializer=TruncatedNormal(), activation='relu'))

    model.add(Dropout(rate=0.5))

    model.add(MaxPooling2D(pool_size=[1, 3],
    strides=[1, 3], padding='same'))

    model.add(BatchNormalization())

    model.add(Convolution2D(filters=64, kernel_size=[10, 4], strides=[1, 1], padding='same', kernel_initializer=TruncatedNormal(stddev=0.01), activation='relu'))

    model.add(Flatten())

    model.add(Dense(32, activation='relu', kernel_initializer=TruncatedNormal(stddev=0.01)))
    model.add(Dense(128, activation='relu', kernel_initializer=TruncatedNormal(stddev=0.01)))
    model.add(Dense(1, activation='sigmoid', kernel_initializer=TruncatedNormal(stddev=0.01)))

    print(model.summary())
    return model
