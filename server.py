from flask import Flask, request, send_file, send_from_directory, abort, jsonify
from flask_cors import CORS
import os
import tensorflow as tf
from utils.textGenerator import textGenerator
from model.textGenerator import TextGenerator

app = Flask(__name__, static_folder='build')
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != '' and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')



@app.route('/api', methods=['GET'])
def ecrivan():
    initialText = request.args.get('inputText')
    wordLimit = request.args.get('wordLimit')
    try:
        story = textGenerator(model, initialText, wordLimit)
    except Exception as error:
        print(error)
        return abort(400)
    
    return jsonify({'story': story})

if __name__ == "__main__":
    graph = tf.get_default_graph()
    model = TextGenerator(graph)
    app.run(port=5000)
