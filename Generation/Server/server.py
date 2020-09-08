import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from flask import Flask, render_template, request
import Drawing.test_seq_style as transform
from PIL import Image


app = Flask(__name__)


@app.route("/")
def main():
    return render_template("show.html")


@app.route("/transform", methods=['POST'])
def transform():
    try:
        image = request.files['image']
        if image:
            # 전달받은 이미지 저장 및 변환
            image.save("./Drawing/examples/" + image.filename)
            transform.seq_style()

            # Drawing 폴더에서 생성된 fake 사진의 이름 지
            img_name = image.filename.split(".")[0] + "_fake.png"
            # javascript로 보낼 사진 이름 리스트
            img_lst = dict()

            # result의 사진들 읽고, Server/static/images로 저장
            for idx, link in enumerate(['0-0-1/', '0-1-0/', '1-0-0/']):
                tf_image = Image.open("./Drawing/results/pretrained/test_200/imagesstyle" + link + img_name)
                tf_dir = "./Server/static/images/" + image.filename.split(".")[0] + "_" + str(idx + 1) + "_fake.png"
                tf_image.save(tf_dir, 'PNG')

                # ../static/images/이미지 이름
                tf_dir = ".." + tf_dir[8:]
                img_lst[idx] = tf_dir

            return img_lst

    except Exception as e:
        print("error : not contain image")
        return Response("fail", status=400)


@app.route("/healthz", methods=["GET"])
def healthCheck():
    return "", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)