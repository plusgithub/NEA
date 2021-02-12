from inputFilter import Filter
import clientServer
import voicebox
import streamer
import yaml
from neurons import getDate, getNews

def startup():
    with open(r'C:\Users\iamar\Wakeword-neural-network\settings.yml') as file:
            settings_file = yaml.full_load(file)
    
    if settings_file["morning"] == True:
        speech = voicebox.Speak()
        speech.add_text("Good morning, sir")
        speech.speak()
    if settings_file["date"] == True:
        speech = voicebox.Speak()
        speech.add_text(getDate.getDate())
        speech.speak()
    if settings_file["news"] == True:
        #readnews
        speech = voicebox.Speak()
        for i in getNews.getNews()["articles"]:
            speech.add_text(str(i['title']))
        speech.speak()

def fromWakeUp():
    information = clientServer.send_information(True)
    filtered = Filter(information)
    returned = filtered.automatic()
    speech = voicebox.Speak()
    speech.add_text(returned)
    speech.speak()
    print(returned)
    fromWakeUp()


def sleeping():
    print("Activating listener...")
    engine = streamer.InferenceEngine(r'C:\Users\iamar\Wakeword-neural-network\wakeword_models\new-model.tflite')
    recorder = streamer.Recorder(None, 900, engine)
    if recorder == True:
        speech = voicebox.Speak()
        speech.add_text("Waiting on your command")
        speech.speak()
        fromWakeUp()
    else:
        sleeping()

fromWakeUp()