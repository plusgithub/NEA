import pyaudio
import sys
import time
import librosa
import numpy as np
from tflite_runtime.interpreter import Interpreter
import wave
import os
import threading
from array import array
from queue import Queue, Full
import argparse

SEC = 1
CHUNK_SIZE = 128
RATE = 16000
NUM_CHUNKS=RATE*SEC/CHUNK_SIZE
BUF_MAX_SIZE = CHUNK_SIZE * 10

class Recorder:

    def __init__(self, threshold, engine):
        self.recording = False
        self.threshold = threshold
        self.stopped = False
        self.engine = engine

        queue = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK_SIZE)))

        listen_thread = threading.Thread(target=self.listen, args=(queue,))
        listen_thread.start()

        record_thread = threading.Thread(target=self.record, args=(queue,))
        record_thread.start()

        try:
            while True:
                if self.stopped:
                    break
                listen_thread.join(0.1)
                record_thread.join(0.1)
        except KeyboardInterrupt:
            self.stopped = True

        listen_thread.join()
        record_thread.join()


    def predict(self, data):#

        data = np.array(data).astype('float')
        print(data)
        data = data.flatten()/32768
        mfcc = librosa.feature.mfcc(data, 16000, n_mfcc=40)
        x = np.reshape(mfcc, [-1, 40, 32, 1])


        predictions = self.engine.infer(x)
        print(predictions)
        return predictions

    def record(self, queue):

        frame_buffer = []
        while True:
            if self.stopped:
                break

            chunk = queue.get()
            vol = max(chunk)
            frame_buffer.append(chunk)

            if self.recording:
                frames.append(chunk)
                if len(frames) >= NUM_CHUNKS:
                   result = self.predict(frames)
                   if result > 0.1:
                       print("Triggered")
                   self.recording = False
            else:
                pass
                
            if vol >= self.threshold and not self.recording:
                self.recording = True
                frames = frame_buffer[-7:]

    def listen(self, queue):
        p = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE,
        )

        while True:
            if self.stopped:
                break
            try:
                queue.put(array('h', p.read(CHUNK_SIZE)))
            except Full:
                pass 

engine = InferenceEngine(r'C:\Users\iamar\Wakeword-neural-network\wakeword_models\new-model.tflite')
recorder = Recorder(900, engine)