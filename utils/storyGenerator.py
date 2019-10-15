def storyGenerator(initialText, wordLimit):
    initialText = initialText + ' '
    wordLimit = int(wordLimit)
    result = initialText* int((wordLimit/len(initialText)))
    return result