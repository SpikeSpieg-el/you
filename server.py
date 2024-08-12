from flask import Flask, render_template, jsonify, send_from_directory, request
import os
from datetime import datetime

app = Flask(__name__)

# Укажите путь к папке, где хранятся файлы
FILE_DIRECTORY = r'C:\Users\chash\Pictures\sd webui\webui\outputs\txt2img-images'

def get_files_and_dirs(directory, sort_by=None, sort_order='asc', search_query=None):
    entries = []
    with os.scandir(directory) as it:
        dirs = []
        files = []
        for entry in it:
            if search_query and search_query.lower() not in entry.name.lower():
                continue
            if entry.is_dir():
                dirs.append({
                    'type': 'directory',
                    'name': entry.name,
                    'path': os.path.relpath(entry.path, FILE_DIRECTORY),
                    'children': get_files_and_dirs(entry.path, sort_by, sort_order, search_query)
                })
            elif entry.is_file():
                files.append({
                    'type': 'file',
                    'name': entry.name,
                    'path': os.path.relpath(entry.path, FILE_DIRECTORY),
                    'size': entry.stat().st_size,
                    'mtime': datetime.fromtimestamp(entry.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'ctime': datetime.fromtimestamp(entry.stat().st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # Сортировка директорий и файлов
        def sort_key(entry):
            if sort_by == 'size':
                return entry.get('size', 0)
            elif sort_by == 'date_created':
                return entry.get('ctime', '')
            elif sort_by == 'date_modified':
                return entry.get('mtime', '')
            else:  # default to name sorting
                return entry.get('name', '').lower()

        if sort_by:
            dirs.sort(key=sort_key, reverse=(sort_order == 'desc'))
            files.sort(key=sort_key, reverse=(sort_order == 'desc'))

        return dirs + files

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/contents')
def contents():
    sort_by = request.args.get('sort_by')
    sort_order = request.args.get('sort_order', 'asc')  # Default to ascending order
    search_query = request.args.get('search_query')
    return jsonify(get_files_and_dirs(FILE_DIRECTORY, sort_by, sort_order, search_query))

@app.route('/files/<path:filename>')
def get_file(filename):
    return send_from_directory(FILE_DIRECTORY, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
