import yaml
from neurons import *
from entityExtraction import take_entities

class Filter():

    def __init__(self, input_string):
        self.hotwords_list = {}
        self.input_string = input_string

        with open(r'C:\Users\iamar\Wakeword-neural-network\hotwords.yml') as file:
            hotword_file = yaml.full_load(file)

            for function, words_list in hotword_file.items():
                self.hotwords_list[function] = words_list

    def create_hotwords(self):
        for x, i in enumerate(self.hotwords_list.values()):
            for o in i:
                if self.input_string.lower().find(o) != -1:
                    return list(self.hotwords_list)[x]
        return


    def automatic(self): 
        function = self.create_hotwords()
        if function != None:
            result = eval(function + "(self)")
            return result
        else:
            return "I don't understand that quite yet"

    def get_string(self):
        return self.input_string

    def extract_entities(self):
        return(take_entities(self.input_string))