import os
import uuid
import subprocess
from flask import Flask, request, jsonify, send_from_directory
from threading import Thread
from pathlib import Path

APP_DIR = Path(__file__).parent
CONV_DIR = APP_DIR / "conversions"
CONV_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
jobs = {}

def run_conversion(job_id, image_files, audio_path):
    try:
        workdir = CONV_DIR / job_id
        workdir.mkdir()
        # Save images in order
        for i, f in enumerate(image_files, start=1):
            ext = Path(f.filename).suffix or '.jpg'
            target = workdir / f"img{i:03d}{ext}"
            f.save(target)
        # Convert all to jpg for consistent sequence
        for f in sorted(workdir.iterdir()):
            dst = f.with_suffix('.jpg')
            subprocess.run(['ffmpeg','-y','-i',str(f), str(dst)], check=True)
        temp_video = workdir / "temp_video.mp4"
        subprocess.run([
            'ffmpeg','-y','-framerate','1','-i', str(workdir / 'img%03d.jpg'),
            '-c:v','libx264','-r','30','-pix_fmt','yuv420p', str(temp_video)
        ], check=True)
        final_out = workdir / "output.mp4"
        if audio_path:
            subprocess.run([
                'ffmpeg','-y','-i', str(temp_video), '-i', str(audio_path),
                '-c:v','copy','-c:a','aac','-shortest', str(final_out)
            ], check=True)
        else:
            temp_video.rename(final_out)
        jobs[job_id]['status'] = 'done'
        jobs[job_id]['out_path'] = str(final_out)
    except Exception as e:
        jobs[job_id]['status'] = 'error'
        jobs[job_id]['error'] = str(e)

@app.route('/api/convert', methods=['POST'])
def convert():
    images = request.files.getlist('images')
    audio = request.files.get('audio')
    job_id = str(uuid.uuid4())
    jobs[job_id] = {'status': 'queued'}
    audio_path = None
    if audio:
        audio_path = CONV_DIR / f"{job_id}_audio{Path(audio.filename).suffix}"
        audio.save(str(audio_path))
    jobs[job_id]['status'] = 'processing'
    thr = Thread(target=run_conversion, args=(job_id, images, audio_path))
    thr.start()
    return jsonify({'job_id': job_id}), 202

@app.route('/api/status/<job_id>')
def status(job_id):
    info = jobs.get(job_id)
    if not info:
        return jsonify({'status':'not_found'}), 404
    return jsonify({'status': info.get('status'), 'error': info.get('error','')})

@app.route('/api/download/<job_id>')
def download(job_id):
    info = jobs.get(job_id)
    if not info or info.get('status') != 'done':
        return "Not ready", 404
    out_path = info['out_path']
    directory, filename = os.path.split(out_path)
    return send_from_directory(directory, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
