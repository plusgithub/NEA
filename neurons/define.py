from PyDictionary import PyDictionary

def defineWord(word):
    dictionary=PyDictionary()
    definition = dictionary.meaning(word)
    return definition