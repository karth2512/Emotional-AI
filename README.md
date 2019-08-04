# Emotional-AI
A chat-bot that uses multiple data points from the interacting person in order to serve as an emotional assistant.

## Voice2Emotion
- Aims to extract emotions from raw voice
- librosa used for loading and preprocessing datasets
- The model is a customized version(derived from [Speech Emotion Analyzer]()) trained over multiple datasets lowering focus on gender.

## Speech2Text
- Using Recognizer class of the [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) Library in Python to access Speech to Text APIs
- This version uses Google Web Speech API


## Datasets:
- [RAVDESS](https://zenodo.org/record/1188976).
- [SAVEE](http://kahlan.eps.surrey.ac.uk/savee/Download.html).