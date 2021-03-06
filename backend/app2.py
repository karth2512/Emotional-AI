from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import base64
import cv2
import numpy as np
from statistics import mode
from keras.models import load_model
from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input
import librosa
import librosa.display
import numpy as np
import tensorflow as tf
from matplotlib.pyplot import specgram
import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.models import Model
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import confusion_matrix
import pyaudio
import wave
from keras.models import model_from_json
import speech_recognition as sr
tf.keras.backend.clear_session()
print("IMPORTED")

#configurations to extract emotion from voice
CHUNK = 1024 
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 2 
RATE = 44100 #sample rate
RECORD_SECONDS = 10

#loading pretrained model from disk
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("saved_models/Emotion_Voice_Detection_Model.h5")

global graph
graph = tf.get_default_graph()

def emotion_voice():
    X, sample_rate = librosa.load('output.wav', res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
    sample_rate = np.array(sample_rate)
    mfccs = np.mean(librosa.feature.mfcc(y=X,sr=sample_rate,n_mfcc=13),axis=0)
    feature = mfccs
    X_test = np.array(feature)
    x_traincnn =np.expand_dims(X_test, axis=2)
    with graph.as_default():
        preds = loaded_model.predict(np.array([x_traincnn]),batch_size=32,verbose=1)
    preds1=preds.argmax(axis=1)
    preds1
    mapper = ["female_angry","female_calm","female_fearful","female_happy","female_sad","male_angry","male_calm","male_fearful","male_happy","male_sad"]
    return (mapper[preds1.tolist()[0]])


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#
def GSpeechAPI():
    r = sr.Recognizer()
    harvard = sr.AudioFile('output.wav')
    with harvard as source:
        audio = r.record(source)
    return(r.recognize_google(audio))

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/voice2emotion', methods=['POST'])
def voice2emotion():
    byte = base64.b64decode(request.form["data"].split(",")[1])
    newFile = open("output.wav", "wb")
    newFile.write(byte)
    newFile.close()
    return emotion_voice()

@app.route('/speech2text', methods=['GET'])
def speech2text():
    print("speech2text")
    return GSpeechAPI()

if __name__ == '__main__':
    app.run(debug=True,port=5001)