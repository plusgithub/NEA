from pathlib import Path
import os
import numpy as np
import librosa

class DataEntry(object):

    def __init__(self, file_path, label):
        self.file_path = file_path
        self.sample_rate = 16000

        if label == 'negative':
            self.label = 0
        if label == 'positive':
            self.label = 1

        self.mfcc_conversion()

    def mfcc_conversion(self):
        samples, sample_rate = librosa.load(self.file_path, sr=self.sample_rate, res_type='kaiser_best')
        self.mfcc = librosa.feature.mfcc(y=samples, sr=sample_rate, n_mfcc=40)