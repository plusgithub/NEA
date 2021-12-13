from playsound import playsound 
import boto3
import os

polly_client = boto3.Session(
    aws_access_key_id="KEY",                     
    aws_secret_access_key="SECRET",
    region_name='eu-west-2').client('polly')

class Speak():

    no_formatting = ''

    def __init__(self, voice="Matthew", language='en-US'):
        self.voice = voice
        self.language = language

    def speak(self):
        text = '<speak>{}</speak>'.format(self.no_formatting)
        print(text)
        response = polly_client.synthesize_speech(VoiceId=self.voice,
                    Engine='neural',
                    OutputFormat='mp3', 
                    Text=text,
                    TextType='ssml')
        file = open('speech.mp3', 'wb')
        file.write(response['AudioStream'].read())
        file.close()
        playsound("speech.mp3")
        os.remove('speech.mp3')

    def add_text(self, text):
        self.no_formatting+=text

    def add_special(self, text, style):
        if style != 'date':
            self.no_formatting+=f'<say-as interpret-as="{style}">{text}</say-as>'
        else:
            self.no_formatting+=f'<say-as interpret-as="date" format="dmy">{text}</say-as>'

    def add_pause(self, amount):
        self.no_formatting+= f'<break time="{amount}"/>'

    def add_whisper(self, text):
        self.no_formatting+= f'<amazon:effect name="whispered">{text}</amazon:effect>'

    def add_style(self, text, style):
        self.no_formatting+= f'<amazon:domain name="{style}">{text}</amazon:domain>'

    def add_breaths(self, text):
        self.no_formatting+= f'<amazon:auto-breaths>{text}</amazon:auto-breaths>'

    def add_soft_text(self, text):
        self.no_formatting+= f'<amazon:effect phonation="soft">{text}</amazon:effect>'
    

