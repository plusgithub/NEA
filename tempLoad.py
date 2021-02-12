import random
from pathlib import Path
import os
import numpy as np
import librosa
from loadData import DataEntry

def load_files(wav_files, file_labels):

    labelled_data = []

    for wav_file in wav_files.iterdir():
        data_entry = DataEntry(str(wav_file), file_labels)
        labelled_data.append(data_entry)

    return labelled_data

def load_data(path):
    print("Loading positive data")
    data_positives = load_files(Path(f'{path}\\positive'), 'positive')
    print("Loading negative data")
    data_negatives = load_files(Path(f'{path}\\negative'), 'negative')

    data = data_negatives + data_positives
    random.shuffle(data)

    x_data = list(map(lambda what : what.mfcc, data))
    x_labels = list(map(lambda what: what.label, data))

    x_data = np.reshape(x_data, [-1, 40, 32, 1])

    print(x_data.shape)
    return(np.array(x_data),  np.array(x_labels))