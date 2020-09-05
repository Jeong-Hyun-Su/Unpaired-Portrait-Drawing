from flask import Flask, render_template, request, send_file
import Drawing.test_seq_style as seq
import cv2
import base64
import json

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("show.html")

@app.route("/transform", methods=['POST'])
def transform():
    try:
        image = request.files['image']
        if image:
            image.save("../Drawing/examples/" + image.filename)
            # seq.seq_style()

            img_name = image.filename.split(".")[0] + "_fake.png"

            send_name = dict()
            for idx, link in enumerate(['0-0-1/', '0-1-0/', '1-0-0/']):
                send_name[idx] = "../static/image/" + image.filename.split(".")[0] + "_" + str(idx+1) + "_fake.png"
                img = cv2.imread("../Drawing/results/pretrained/test_200/imagesstyle" + link + img_name)

                cv2.imwrite(send_name[idx], img)
                send_name[idx] = send_name[idx]

    except KeyError:
        return "null"

    return send_name

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)