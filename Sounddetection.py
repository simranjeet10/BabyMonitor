import librosa
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import joblib

# set directory containing audio files
audio_dir = r'C:/Users/dell/Desktop/AShish/babymonitor/audio'

# get list of audio file paths
audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith('.wav')]

# create empty lists to store features and labels
features = []
labels = []

# loop over audio files and extract features
for audio_file in audio_files:
    # load audio file and extract features
    y, sr = librosa.load(audio_file, res_type='kaiser_fast')
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    
    # append features and labels to lists
    features.append(mfccs)
    labels.append(1)  # assuming all audio files contain baby crying sounds

# convert features and labels to numpy arrays
X = np.array(features)
y = np.array(labels)

# split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train support vector machine classifier
svm = SVC(kernel='linear', probability=True, random_state=42)
svm.fit(X_train.reshape(X_train.shape[0], -1), y_train)

# save SVM classifier as HDF5 file
joblib.dump(svm, 'svm_model.h5')

# load SVM classifier from HDF5 file
svm_loaded = joblib.load('svm_model.h5')

# predict labels of new audio file
new_audio_file = 'path/to/new/audio/file.wav'
y_new, sr_new = librosa.load(new_audio_file, res_type='kaiser_fast')
mfccs_new = librosa.feature.mfcc(y=y_new, sr=sr_new, n_mfcc=20)
X_new = mfccs_new.reshape(1, -1)
y_pred = svm_loaded.predict(X_new)

print('Prediction:', y_pred)
