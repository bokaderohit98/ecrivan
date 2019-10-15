def textGenerator(model, initialText, wordLimit):
    wordLimit = int(wordLimit)
    print(wordLimit - 100)
    result = model.predict(initialText, wordLimit)
    return result