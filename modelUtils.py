import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, MaxPooling2D, Bidirectional, Reshape, BatchNormalization, Convolution2D, Flatten, Dense
from tensorflow.keras.initializers import TruncatedNormal
import numpy as np

def compile_model(model, epochs, train_data, train_labels, validation_data, validation_labels):

    model.compile(
        loss='binary_crossentropy',
        optimizer=keras.optimizers.Adam(amsgrad=True), metrics=['accuracy'])

    early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', patience=50,
                     verbose=1, mode='min', baseline=None, restore_best_weights=True)

    return model.fit(
        train_data, train_labels,
        callbacks=[early_stopping],
        validation_data=(validation_data, validation_labels),
        epochs=epochs,
        verbose=1,
        batch_size=200
        )

def evaluate_model(model, evaluation_data, evaluation_labels):
    score = model.evaluate(evaluation_data, evaluation_labels, verbose=1)

    print('Model evaluation:')
    print(model.metrics_names[0] + ': ' + str(score[0]))
    print(model.metrics_names[1] + ': ' + str(score[1]))
    for index in list(range(30)):
        test = evaluation_data[index]
        test = np.reshape(test, [1, 40, 32, 1])
        res = model.predict(test, verbose=1)


        print('Label: ' + str(evaluation_labels[index]) + ' | ' + str(res))

    return score[1]

def save_model(model, evaluation_accuracy):

    model_filename = r'C:\Users\iamar\wakeword-models\wakeword-model.h5'
    model.save(model_filename)

    return model_filename