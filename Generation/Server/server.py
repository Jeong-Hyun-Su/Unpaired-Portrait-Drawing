import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from flask import Flask, render_template, request, Response, send_file, jsonify
from queue import Queue, Empty
import threading
import time

# from Drawing import test_seq_style as transform
from Drawing import test
from Drawing import make_model as model

# Make 3 Models
models = dict()
for styles in ["1-0-0", "0-1-0", "0-0-1"]:
    models[styles] = model.make_model(styles)

os.chdir("/workspace/Generation")

# Server & Handling Setting
app = Flask(__name__)

requests_queue = Queue()
BATCH_SIZE = 1
CHECK_INTERVAL = 0.1


# Queue 핸들링
def handle_requests_by_batch():
    while True:
        requests_batch = []
        while not (len(requests_batch) >= BATCH_SIZE):
            try:
                requests_batch.append(requests_queue.get(timeout=CHECK_INTERVAL))
            except Empty:
                continue

            for requests in requests_batch:
                requests['output'] = run(requests['input'][0], requests['input'][1])


# 쓰레드
threading.Thread(target=handle_requests_by_batch).start()


@app.route("/")
def main():
    return render_template("show.html")


# Sketch Start
def run(image, style):
    # 전달받은 이미지 저장 및 변환
    image.filename = "input.png"
    file_dir = "./Drawing/examples/" + image.filename

    image.save(file_dir)
    # "1-0-0" => [1, 0, 0] 변환
    try:
        vec = list(map(int, style.split("-")))
    except Exception:
        # 전달되지 않을 경우, 기본으로 세팅
        vec = [1, 0, 0] 
        
    svec = '%d,%d,%d' % (vec[0], vec[1], vec[2])
    # Make a Fake Image
    os.chdir("/workspace/Generation/Drawing")
    val = test.app(models[style], svec)
    os.chdir("/workspace/Generation")

    # 사진 체크 후 삭제
    if os.path.isfile(file_dir):
        os.remove(file_dir)

    return val


@app.route("/transform", methods=['POST'])
def sketch():
    # 큐에 쌓여있을 경우,
    if requests_queue.qsize() > BATCH_SIZE:
        return jsonify({'error': 'TooManyReqeusts'}), 429

    # 웹페이지로부터 이미지와 스타일 정보를 얻어옴.
    try:
        image = request.files['image']
        style = request.form['style']

        if style == 'Style 1':
            style = '1-0-0'
        elif style == 'Style 2':
            style = '0-1-0'
        elif style == 'Style 3':
            style = '0-0-1'

    except Exception:
        print("error : not contain image")
        return Response("fail", status=400)

    # Queue - put data
    req = {
        'input': [image, style]
    }
    requests_queue.put(req)

    # Queue - wait & check
    while 'output' not in req:
        time.sleep(CHECK_INTERVAL)

    # Get Result & Send Image
    byte_io = req['output']
    return send_file(byte_io, mimetype="image/png")


# Health Check
@app.route("/healthz", methods=["GET"])
def healthCheck():
    return "", 200


if __name__ == "__main__":
    from waitress import serve
    serve(app, host='0.0.0.0', port=80)
