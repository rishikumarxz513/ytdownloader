from flask import Flask, request, jsonify, render_template
from pytubefix import YouTube
import os
import re
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)
progress = 0

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/progress')
def get_progress():
    global progress
    return jsonify({'progress': progress})

@app.route('/thumbnail', methods=['POST'])
def get_thumbnail():
    data = request.json
    url = data.get('url')
    yt = YouTube(url)
    thumbnail_url = yt.thumbnail_url
    return jsonify({'thumbnail': thumbnail_url})

@app.route('/video-options', methods=['POST'])
def video_options():
    data = request.json
    url = data.get('url')
    yt = YouTube(url)
    streams = yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
    options = [stream.resolution for stream in streams]
    return jsonify({'options': options})

@app.route('/download', methods=['POST'])
def download_video_or_audio():
    global progress
    data = request.json
    url = data.get('url')
    choice = data.get('choice')
    quality = data.get('quality', None)
    
    print(f"Received URL: {url}")
    print(f"Download choice: {choice}")
    print(f"Selected quality: {quality}")

    try:
        yt = YouTube(url)
        thumbnail_url = yt.thumbnail_url
        response = {'thumbnail': thumbnail_url, 'progress': 0, 'message': ''}

        if choice == 'audio':
            stream = yt.streams.filter(only_audio=True).first()
        else:
            streams = yt.streams.filter(file_extension='mp4', resolution=quality).order_by('resolution').desc()
            if not streams:
                response['message'] = "No available video streams found."
                return jsonify(response)
            stream = streams.first()
        
        file_size = stream.filesize
        progress = 0
        
        # Specify the download folder
        download_folder = r"C:\Users\Rishikesh\Downloads\project"
        
        # Create the download folder if it doesn't exist
        os.makedirs(download_folder, exist_ok=True)
        
        filename = os.path.join(download_folder, sanitize_filename(yt.title) + ".mp4")
        
        stream_response = requests.get(stream.url, stream=True)
        with open(filename, 'wb') as f:
            total_chunks = file_size // 1024
            for i, chunk in enumerate(stream_response.iter_content(chunk_size=1024)):
                if chunk:
                    f.write(chunk)
                    progress = int((i / total_chunks) * 100)
        
        response['message'] = f'Download complete: {yt.title}'
        progress = 100
    except Exception as e:
        response['message'] = f"Failed to download: {str(e)}"
        print(f"Error: {e}")
        progress = 0

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
