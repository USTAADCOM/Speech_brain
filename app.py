"""
Main module of flask API.
"""
# Third party modules
from typing import Any
from functools import wraps
import os
import datetime
from dotenv import load_dotenv
import threading
import speechbrain as sb
from speechbrain.dataio.dataio import read_audio, write_audio
from speechbrain.pretrained import EncoderDecoderASR
from flask import (
    Flask, request,
    json, make_response, Response
)
from flask_cors import CORS, cross_origin
# Module
from modules import speech_to_text_module
from modules import text_to_speech_module

app = Flask(__name__)
cors = CORS(app)
app.config['PROPAGATE_EXCEPTIONS'] = True
speech_folder = 'temp'
def authorize(token: str)-> bool:
    """
    method take header token as input and check valid ot not.

    Parameters:
    ----------
    toekn: str 
        token pass by the user in header.

    Return:
    ------
        return True if the toekn is valid otherwise return False.

    """
    load_dotenv()
    my_key = os.getenv('api-key')
    if token != my_key:
        return True
    return False

def token_required(func: Any)-> Any:
    """
    method token required will perform the authentication based on taoken.

    Parameters:
    ----------
    func: Any
        arguement ass to the function from request header.

    Return:
    ------
        return the the response of the token authentication.

    """
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'api-key' not in request.headers:
            result = make_response(json.dumps(
            {'message'  : 'Authorization error',
            'category' : 'Bad Params',}),
            400)
            return result
        token = request.headers['api-key']
        if not token:
            result = make_response(json.dumps(
            {'message'  : 'Authorization error',
            'category' : 'Bad Params',}),
            400)
            return result
        if authorize(token):
            result = make_response(
            json.dumps(
            {'message'  : 'Invalid Key',
            'category' : 'Authorization error',}),
            401)
            return result
        return func(*args, **kwargs)
    return decorated

@app.errorhandler(404)
def not_found(e)-> Response:
    """
    method check the request and if Not found issue 
    occure it will return a response.

    Parameters
    ----------
    e: Any
        contain the request.

    Return
    ------
    result: json
        json response containing the error code and message.

    """
    result = make_response(
        json.dumps(
        {'message'  : 'page not found',
        'category' : 'Not Found'}),
        404)
    return result

@app.errorhandler(500)
def server_error(e)-> Response:
    """
    method check the request and if any internal server issue 
    found it will return a response.

    Parameters
    ----------
    e: Any
        contain the request.

    Return
    ------
    result: json
        json response containing the error code and message.

    """
    result = make_response(
        json.dumps(
        {'message'  : 'Internal Server Error',
        'category' : 'Bad Request'}),
        500)
    return result
def validate_text_request(request_api: Any)-> bool:
    """
    method will take a json request and perform all validations if the any error 
    found then return error response with status code if data is correct then 
    return data in a list.

    Parameters
    ----------
    request_api: Request
        contain the request data in file format.

    Return
    ------
    bool
        return True or False.

    """
    data = request_api.get_json()
    if "text_data" in data:
        if data["text_data"] == '':
            return False
        return True
    if "text_data" not in data:
        return False

def validate_request(request_api: Any)-> bool:
    """
    method will take a json request and perform all validations if the any error 
    found then return error response with status code if data is correct then 
    return data in a list.

    Parameters
    ----------
    request_api: Request
        contain the request data in file format.

    Return
    ------
    bool
        return True or False.

    """
    if "speech_file" in request_api.files:
        if request_api.files['speech_file'].filename == '':
            return False
        return True
    if "speech_file" not in request_api.files:
        return False

def get_file(speech_file: str)-> str:
    """
    method will take request and get file path and return it .

    Parameters
    ----------
    file_path: str
        contain the requested file path.

    Return
    ------
    speech_file: str
        return the speech file path as string.

    """
    return speech_file
def get_textdata(data: json)-> str:
    """
    method will take a json data and return text_data.

    Parameters:
    ----------
    data: json
        json data send in request.

    Return:
    ------
    text_data: str
        return text_data as string.

    """
    text_data = data["text_data"]
    return text_data
def save_file(request_api: Any)-> str:
    """
    method will take request and save file from request in specified folder.

    Parameters:
    ----------
    request_api: Request
        contain the request data in file format.

    Return:
    ------
    save_file_path: str
        file path save on our local sever.
    """
    image_f = request_api.files["speech_file"]
    time_stamp_name = str(datetime.datetime.now().timestamp()).replace(".", "")
    image_list = image_f.filename.split(".")
    image_extension = image_list[len(image_list)-1]
    save_file_path = f"{speech_folder}/{time_stamp_name}.{image_extension}"
    image_f.save(save_file_path)
    return save_file_path
def make_bad_params_value_response()-> Response:
    """
    method will make a error response a return it back.

    Parameters:
    ----------
    None

    Return:
    ------
    Response
        return a response message.

    """
    result = make_response(json.dumps(
        {'message'  : 'No Speech Provided',
        'category' : 'Bad Params',}),
        400)
    return result
def make_bad_params_text_key_response()-> Response:
    """
    method will make a error response a return it back.

    Parameters:
    ----------
    None

    Return:
    ------
    Response
        return a response message.

    """
    result = make_response(json.dumps(
        {'message'  : 'text_data error',
        'category' : 'Bad Params',}),
        400)
    return result

def make_bad_params_key_response()-> Response:
    """
    method will make a error response a return it back.

    Parameters:
    ----------
    None

    Return:
    ------
    Response
        return a response message.

    """
    result = make_response(json.dumps(
        {'message'  : 'speech_file error',
        'category' : 'Bad Params',}),
        400)
    return result

def make_invalid_extension_response()-> Response:
    """
    method will make a error response a return it back.

    Parameters:
    ----------
    None

    Return:
    ------
    Response
        return a response message.

    """
    result = make_response(json.dumps(
        {'message'  : 'Invalid Extension',
        'category' : 'Bad Params',}),
        400)
    return result

def validate_extension(request_api: Any)-> bool:
    """
    method will take image and check its extension is .jpg, .jpeg, .png.

    Parameters
    ----------
    image: Any
        image recieved in API request.

    Return
    ------
    bool
        return the true or false image is has valid extension or not.

    """
    speech_f = request_api.files["speech_file"]
    speech_list = speech_f.filename.split(".")
    speech_extension = speech_list[len(speech_list)-1]
    speechs_extensions = ['wav', 'flac', 'mp3']
    if speech_extension in speechs_extensions:
        return True
    return False

@app.route('/speechToText', methods = ['POST'])
@token_required
@cross_origin()
def convert_speech_to_text()-> Response:
    """
    method will take the data and return the speech_file from request
    and return its text as json response.

    Parameters:
    ----------
    None

    Return:
    ------
    str
        return the prediction of the model.

    """
    try:
        if validate_request(request):
            if validate_extension(request):
                speech_path = save_file(request)
                speech_file = get_file(speech_path)
                predicted_data = speech_to_text_module.speech_to_text(speech_file)
                return Response(
                    json.dumps(predicted_data),
                    mimetype = 'application/json'
                    )
            return make_invalid_extension_response()
        return make_bad_params_key_response()
    except Exception as exception:
        return exception
@app.route('/textToSpeech', methods = ['POST'])
@token_required
@cross_origin()
def convert_text_to_speech()-> Response:
    """
    method will take the data and return the speech_file from request
    and return its text as json response.

    Parameters:
    ----------
    None

    Return:
    ------
    str
        return the prediction of the model.

    """
    try:
        if validate_text_request(request):
            print("In method")
            query = request.get_json()
            text_data = get_textdata(query)
            predicted_data = text_to_speech_module.text_to_speech(text_data)
            return Response(
                json.dumps(predicted_data),
                mimetype = 'application/json'
                )
        return make_bad_params_text_key_response()
    except Exception as exception:
        return exception
if __name__=='__main__':
    app.run(debug = True, threaded = True)
