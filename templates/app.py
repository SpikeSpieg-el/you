from flask import Flask, render_template, request
import requests
import socket

app = Flask(__name__)
API_KEY = 'AIzaSyAIuRRH4V1aofNSGCV1DLTqAkQ5Jtrm-tk'
SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('query') or ''
    videos = []
    if request.method == 'POST' or query:
        query = request.form.get('query') or query
        if query:
            response = requests.get(SEARCH_URL, params={
                'part': 'snippet',
                'q': query,
                'key': API_KEY,
                'type': 'video',
                'maxResults': 10
            })
            if response.status_code == 200:
                data = response.json()
                for item in data.get('items', []):
                    if 'videoId' in item['id']:
                        video = {
                            'title': item['snippet']['title'],
                            'video_id': item['id']['videoId'],
                            'thumbnail': item['snippet']['thumbnails']['high']['url'],
                            'published_at': item['snippet']['publishedAt'][:10]
                        }
                        videos.append(video)
    return render_template('index.html', videos=videos, query=query)

@app.route('/video/<video_id>')
def video(video_id):
    query = request.args.get('query', '')
    return render_template('video.html', video_id=video_id, query=query)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    local_ip = get_local_ip()
    print(f"Сайт доступен по адресу: http://{local_ip}:5000/")
    app.run(host='0.0.0.0', port=5000, debug=True)
