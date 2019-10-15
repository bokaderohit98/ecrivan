import numpy as np 
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import pickle

class TextGenerator:
    '''Text Generator model class for predicting text'''

    def __init__(self):
        with open('../cache/charToNMapping.pkl', 'rb') as file:
            self.charToN = pickle.load(file)

        with open('../cache/NToCharMapping.pkl', 'rb') as file:
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
        self.model.load_weights('./textGenerator.weights.h5')

    def encode(self, initialText):
        inputText = initialText[-100:]
        inputTensor = [self.charToN[char] for char in inputText]
        return inputTensor

    def decode(self, initialText, generatedTensor):
        generatedTensor = [self.NToChar[i] for i in generatedTensor]
        return initialText + ''.join(generatedTensor)

    def predict(self, initialText, wordLimit):
        inputTensor = self.encode(initialText)
        generatedTensor = []
        charsToGenerate = wordLimit - len(initialText)

        for i in range(charsToGenerate):
            x = np.reshape(inputTensor, (1, len(inputTensor), 1))
            x = x / self.nChars

            predIndex = np.argmax(self.model.predict([x]))
            generatedTensor.append(predIndex)
            inputTensor.append(predIndex)
            inputTensor = inputTensor[-100:]

        generatedText = self.decode(initialText, generatedTensor)
        return generatedText


        

        

def main():
    model = TextGenerator()
    initialText = '''the riper should by time decease,\n his tender heir might bear his memory:\n but thou, contracted to the world's false sporoe,\n with eyes so dond touls be thy domfornds,\n which for'''
    print(model.predict(initialText, 250))


if __name__ == '__main__':
    main()