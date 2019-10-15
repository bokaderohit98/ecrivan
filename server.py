from flask import Flask, request, send_file, send_from_directory, abort
from flask_cors import CORS

app = Flask(__name__, static_folder='build')
CORS(app)

@app.route('/api', methods=['GET'])
def ecrivan():
    return 'Hello Ecrivan'

if __name__ == "__main__":
    app.run(debug=True, port=5000)
