import spacy
from spacy import displacy

def take_entities(string):
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(string)
    return([(X.text, X.label_) for X in doc.ents])