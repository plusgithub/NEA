from inputFilter import Filter
import clientServer
import voicebox
import streamer
import yaml
from neurons import getDate, getNews
import socket



def startup():
    with open(r'C:\Users\iamar\Wakeword-neural-network\settings.yml') as file:
            settings_file = yaml.full_load(file)
    
    if settings_file["morning"] == True:
        speech = voicebox.Speak()
        speech.add_text("Good morning, sir")
        speech.speak()
    if settings_file["date"] == True:
        speech = voicebox.Speak()
        speech.add_text(getDate.getDate(Filter("yeet")))
        speech.speak()
    if settings_file["news"] == True:
        #readnews
        speech = voicebox.Speak()
        for i in getNews.getNews()["articles"]:
            speech.add_text(str(i['title']))
        speech.speak()

def fromWakeUp(clientSocket):
    information = clientServer.send_information(clientSocket)
    filtered = Filter(information)
    returned = filtered.automatic()
    speech = voicebox.Speak()
    speech.add_text(returned)
    speech.speak()
    print(returned)
    sleeping()


def sleeping():
    print("Activating listener...")
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print('Connecting...')
        clientSocket.connect(('192.168.50.60', 8000)) #Connect to the server
        print(f'Connected to server')
    except Exception as e:
        print(f'Could not connect to server: {e}')

    engine = streamer.InferenceEngine(r'C:\Users\iamar\Wakeword-neural-network\wakeword_models\new-model.tflite')
    recorder = streamer.Recorder(None, 900, engine)

    if recorder.triggered == True:
        speech = voicebox.Speak()
        speech.add_text("Waiting on your command")
        speech.speak()
        fromWakeUp(clientSocket)
    else:
        sleeping()

startup()
sleeping()
#fromWakeUp()