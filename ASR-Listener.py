import socket
import wave
import nemo
import nemo.collections.asr as nemo_asr
#import threading
import nemo.collections.nlp as nemo_nlp
from cryptography.fernet import Fernet

key = Fernet(b'1T09Fq3d0BcKtEAuQbv3zzWuzPiPK2PnzLGO-0yQJ7k=')

data_array = []
OUTPUT_FILE = "output.wav"
FINISHED = False
audio = ['output.wav']
asr_model = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="QuartzNet15x5Base-En")
nlp_model = nemo_nlp.models.PunctuationCapitalizationModel.from_pretrained(model_name='Punctuation_Capitalization_with_DistilBERT')

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create TCP server socket

try:
    serverSocket.bind(('192.168.86.248', 8000)) #Bind the socket to the servers IP
    print("Successfully binded, listening for information")
except Exception as e:
    print(f'Could not bind: {e}')

def performing(clientConnected, clientAddress, serverSocket):
    FINISHED = False
    data_array = []
    while FINISHED == False:
        print(f"DATA RECEIVED FROM {clientAddress[0]}:{clientAddress[1]}") #Print connection information
        data = clientConnected.recv(8192)
        #print(key.decrypt(data))
        try:
            if data.decode() == "END" or data.decode() == "END_NLP":
                FINISHED = True
                print(FINISHED)
        except:
            data_array.append(data) #recieve sent information
            print("DATA CHUNK RECEIVED")


        #clientConnected.send("Return message".encode()) #return encoded message
    if FINISHED == True:
        wf = wave.open(OUTPUT_FILE, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(b''.join(data_array))
        wf.close()
        print(data.decode())
        if data.decode() == "END_NLP":
            clientConnected.send(nlp_model.add_punctuation_capitalization(queries=asr_model.transcribe(paths2audio_files=audio))[0].encode())
        else:
            clientConnected.send(asr_model.transcribe(paths2audio_files=audio)[0].encode())
        print("FINISHED TRANSLATION")
    listener(serverSocket)
        #clientConnected.close()

def listener(serverSocket):
    serverSocket.listen() #wait for data

    clientConnected, clientAddress = serverSocket.accept() #Accept connections
    print(f"Connection request from {clientAddress[0]}:{clientAddress[1]}")
    performing(clientConnected, clientAddress, serverSocket)

#clientConnected.close()
listener(serverSocket)