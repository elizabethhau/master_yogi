from flask import Flask, render_template, Response
from camera import VideoCamera
# import main

app = Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")

@app.route('/')
def index():
  return render_template('index.html')

def generate(camera):
  while True:
    frame = camera.get_frame()
    yield(b'--frame\n'
    b'Content-Type: image/jpeng\n\n' + frame + b'\n\n')

@app.route('/video_feed')
def video_feed():
  return Response(generate(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

# class VideoCamera(object):
#   def __init__(self) -> None:
#       self.video = cv2.VideoCapture(0)

#   def __del__(self):
#     self.video.release()

#   def get_frame(self):
#     ok, frame = self.video.read()
#     ok, jpeg = cv2.imencode('.jpg', frame)
#     return jpeg.tobytes()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port='8000', debug=True)