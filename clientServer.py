import pyaudio
import socket
import time
from cryptography.fernet import Fernet
import numpy


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_information(nlp=True):
    CHUNK = 8192
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 15
    WAVE_OUTPUT_FILENAME = "output.wav"
    THRESHOLD = 100
    INCREMENT=0
    INCREMENT_LAG=3
    key = Fernet(b'1T09Fq3d0BcKtEAuQbv3zzWuzPiPK2PnzLGO-0yQJ7k=')
    vad_true = 0
    p = pyaudio.PyAudio()
    try:
        print('Attempting to connect...')
        clientSocket.connect(('192.168.86.248', 8000)) #Connect to the server
        print(f'Connected to server')
    except Exception as e:
        print(f'Could not connect to server: {e}')



    input("Click enter to start recording")
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("STARTED RECORDING")

    for i, o in enumerate(range(0, int(RATE / CHUNK * RECORD_SECONDS))):
        #data = key.encrypt(stream.read(CHUNK))
        data = stream.read(CHUNK)
        print("VAD PROCESS STARTED")
        vad_value = numpy.average(numpy.abs(numpy.frombuffer(data,dtype=numpy.int16)))*3
        if int(vad_value) < THRESHOLD:
            if vad_true > 0: INCREMENT += 1; print(f"INCREMENT INCREASE TO {INCREMENT}/{INCREMENT_LAG}")
        else:
            INCREMENT = 0
            vad_true = 1
            print(vad_true)
        if INCREMENT >= INCREMENT_LAG:
            p.terminate()
            break
        clientSocket.send(data)
        print(f"CHUNK SENT: {o}     AUDIO VALUE: {vad_value}")

    if nlp == True:
        clientSocket.send("END_NLP".encode())
    else:
        clientSocket.send("END".encode())
    t1 = time.perf_counter()
    print("FINISHED RECORDING")

    t2 = time.perf_counter()
    print(f"Time taken: {round((t2 - t1), 4)}")

    stream.stop_stream()
    stream.close()
    p.terminate()
    return(clientSocket.recv(1024).decode())
