"""
Module contain the functionalities about the speech processing models loading and 
perform these functionalities.
"""
import pickle
import speechbrain as sb
from flask import Response

def load_model():
    """
    method will load the model and return loaded model.

    Parameters:
    ----------
    None

    Return:
    ------
    model: Any
        return the model object loaded from speech_to_text_model.pkl file.

    """
    try:
        model = pickle.load(open('speech_to_text_model.pkl','rb'))
        return model
    except Exception as exception:
        return exception

def speech_to_text(speech_file)-> dict:
    """
    method will take the speec_file and return its text by using the SpeechBrain 
    model.

    Parameters:
    ----------
    None

    Return:
    ------
    str
        return the prediction of the text of speech file as a dictionary.

    """
    model = load_model()
    result = model.transcribe_file(speech_file)
    output_dict = {}
    output = {
            'speech_file' : speech_file,
            'text' : result
            }
    output_dict["output"] = output
    return output_dict
