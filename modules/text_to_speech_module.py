"""
Module contain the functionalities about the speech processing models loading and 
perform these functionalities.
"""
import pickle
import speechbrain as sb
from speechbrain.dataio.dataio import write_audio

def load_model_encoder():
    """
    method will load the model and return loaded model text_to_speech_encoder_model.

    Parameters:
    ----------
    None

    Return:
    ------
    model: Any
        return the model object loaded from text_to_speech_encoder_model.pkl file.

    """
    model_encoder = pickle.load(open('text_to_speech_encoder_model.pkl','rb'))
    return model_encoder

def load_model_decoder():
    """
    method will load the model and return loaded model text_to_speech_converter_model.

    Parameters:
    ----------
    None

    Return:
    ------
    model: Any
        return the model object loaded from text_to_speech_converter_model.pkl file.

    """
    model_decoder = pickle.load(open('text_to_speech_converter_model.pkl','rb'))
    return model_decoder

def text_to_speech(text_data)-> dict:
    """
    method will take the text_data and return its speech file by using the 
    SpeechBrain model.

    Parameters:
    ----------
    None

    Return:
    ------
    str
        return the speech file of text data  as audio .wav file.

    """
    model_encoder = load_model_encoder()
    model_decoder = load_model_decoder()
    mel_output, mel_length, alignment = model_encoder.encode_text(text_data)
    waveforms = model_decoder.decode_batch(mel_output)
    tmpfile = "ekkel.wav"
    write_audio(tmpfile, waveforms.detach().squeeze(), 20000)
    output_dict = {}
    output = {
            'text_data' : text_data,
            'speech_file' : text_data
            }
    output_dict["output"] = output
    return output_dict
