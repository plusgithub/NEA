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

class InferenceEngine:

  def __init__(self, model_file):
    self.interpreter = Interpreter(model_file)
    self.interpreter.allocate_tensors()
    self.tensor_index = self.interpreter.get_input_details()[0]['index']
    _, self.height, self.width, _ = self.interpreter.get_input_details()[0]['shape']

  def infer(self, data):
    start_time = time.time()
    self.interpreter.set_tensor(self.tensor_index, data)
    self.interpreter.invoke()
    output_details = self.interpreter.get_output_details()[0]
    output = np.squeeze(self.interpreter.get_tensor(output_details['index']))

    # If the model is quantized (uint8 data), then dequantize the results
    if output_details['dtype'] == np.uint8:
      scale, zero_point = output_details['quantization']
      output = scale * (output - zero_point)

    elapsed_ms = (time.time() - start_time) * 1000
    print("Inference time: ", elapsed_ms)

    return output


class Recorder:

    def __init__(self, source, threshold, engine):
        self.recording = False
        self.min_volume = threshold
        self.engine = engine
        self.source = source
        self.stoped = False
        self.triggered = False

        q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK_SIZE)))

        if self.source:
            listen_t = threading.Thread(target=self.play, args=(q,))
        else:
            listen_t = threading.Thread(target=self.listen, args=(q,))
        listen_t.start()

        record_t = threading.Thread(target=self.record, args=(q,))
        record_t.start()

        while self.triggered == False:
            print("Triggered = False")
            if self.stoped:
                break
            listen_t.join(0.1)
            record_t.join(0.1)

        print("Triggered = True")
    
        #return True


    def predict(self, data):

        data = np.array(data).astype(np.float32)
        data = data.flatten()/32768
        mfcc = librosa.feature.mfcc(data, 16000, n_mfcc=40)
        x = np.reshape(mfcc, [-1, 40, 32, 1])
        predictions = self.engine.infer(x)
        print(predictions)
        return predictions

    def record(self, q):

        frame_buffer = []
        while True:
            if self.stoped:
                break
            chunk = q.get()
            vol = max(chunk)
            frame_buffer.append(chunk)

            if self.recording:
                frames.append(chunk)
                if len(frames) >= NUM_CHUNKS:
                   result = self.predict(frames)
                   if result > 0:
                       print("Triggered")
                       self.triggered = True
                       return True
                   self.recording = False
            else:
                pass
                
            if vol >= self.min_volume and not self.recording:
                self.recording = True
                frames = frame_buffer[-7:]
     

    def play(self, q):
        wf = wave.open(self.source, 'rb')
        data = wf.readframes(CHUNK_SIZE)
        while data != b'':
            try:
                q.put(array('h', data))
            except Full:
                pass  # discard
            data = wf.readframes(CHUNK_SIZE)
        self.stoped = True

    def listen(self, q):
        stream = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE,
        )

        while True:
            if self.stoped:
                break
            try:
                q.put(array('h', stream.read(CHUNK_SIZE)))
            except Full:
                pass 
