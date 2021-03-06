import numpy as np 
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import pickle

class TextGenerator:
    '''Text Generator model class for predicting text'''

    def __init__(self, graph):
        self.graph = graph

        with open('./cache/charToNMapping.pkl', 'rb') as file:
            self.charToN = pickle.load(file)

        with open('./cache/nToCharMapping.pkl', 'rb') as file:
            self.NToChar = pickle.load(file)

        self.nChars = len(self.charToN)

        self.model = Sequential();
        self.model.add(LSTM(400, input_shape=(100, 1), return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(400, return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(400))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(38, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam')
        self.model.load_weights('./model/textGenerator.weights.h5')

    def encode(self, initialText):
        try:
            inputText = initialText[-100:].lower()
            inputTensor = [self.charToN[char] for char in inputText]
        except Exception as error:
            print(error)
        return inputTensor

    def decode(self, initialText, generatedTensor):
        try:
            generatedTensor = [self.NToChar[i] for i in generatedTensor]
        except Exception as error:
            print(error)
        return initialText + ''.join(generatedTensor)

    def predict(self, initialText, wordLimit):
        try:
            inputTensor = self.encode(initialText)
            generatedTensor = []
            charsToGenerate = wordLimit - len(initialText)

            with self.graph.as_default():
                for i in range(charsToGenerate):
                    x = np.reshape(inputTensor, (1, len(inputTensor), 1))
                    x = x / self.nChars

                    predIndex = np.argmax(self.model.predict([x]))
                    generatedTensor.append(predIndex)
                    inputTensor.append(predIndex)
                    inputTensor = inputTensor[-100:]

            generatedText = self.decode(initialText, generatedTensor)
        except Exception as error:
            print(error)
        return generatedText