from flask import Flask, jsonify, send_from_directory, render_template, abort
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Разрешить CORS для всех доменов

DIRECTORY = r'C:\Users\chash\Pictures\sd webui\webui\outputs\txt2img-images'

def get_files_info(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            stat = os.stat(filepath)
            relative_path = os.path.relpath(filepath, directory)
            files.append({
                'name': filename,
                'path': relative_path,
                'mtime': stat.st_mtime,
                'size': stat.st_size
            })
    files.sort(key=lambda x: x['mtime'], reverse=True)
    return files

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/files', methods=['GET'])
def list_files():
    files_info = get_files_info(DIRECTORY)
    return jsonify(files_info)

@app.route('/files/<path:filename>', methods=['GET'])
def serve_file(filename):
    filepath = os.path.join(DIRECTORY, filename)
    if not os.path.isfile(filepath):
        abort(404)  # Файл не найден
    return send_from_directory(DIRECTORY, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
