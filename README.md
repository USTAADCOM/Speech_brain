# Speech_brain 
Here we develop Speech Generative project which conatin the folowing tools.
* Text To Speech 
* Speech To Text
* Speech Enhancement
## Setup
  ```code
  conda create -n <env_name>
  conda activate <env_name>
  git clone https://github.com/USTAADCOM/Speech_brain.git
  cd Speech_brain
  pip install -r requirements.txt -q
  ```
## Download Models
  ```code
  bash download_ckpt.sh
```
## create .env

* api-key = secret key here
* CLOUD_NAME = cloud name (cloudinary)
* API_KEY = cloudinary api key
* API_SECRET = cloudinary secret phrase

## Project Structure
```bash
Speech_brain
│   .env
│   .gitignore
│   app.py
│   lint-requirements.txt
│   pyproject.toml
│   README.md
│   requirements.txt
│   setup.py
│
└───modules
    │   speech_to_text_module.py
    │   text_to_speech_module.py
    │
```
## Text To Speech 
Payload
```code
{
    "text_data" : "Your string here"
}
```
Response 
```code
{
    'text_data': 'Input string', 
    'speech_file': 'speech file path'
}
```
 
## Speech To Text 
Payload
```code
{
    "speech_file" : "speech_file_source"
}
```
Response 
```code
{
    'speech_file': 'input speech_file path', 
    'text': 'text output from speech file'
}
```
## Run Tool
```code
 python3 app.py
```
