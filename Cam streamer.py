import cv2
from flask import Flask, Response
from pyngrok import ngrok

ngrok.set_auth_token("3EqkXY8qdNNU180ckcBjlgbP1Ow_o4yDJ1p45v1nEjFVD3ob")

app = Flask(__name__)
cap = cv2.VideoCapture(0)

def generate():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/stream')
def stream():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

public_url = ngrok.connect(5000)
print("STREAM URL:", public_url.public_url + "/stream")

app.run(port=5000)