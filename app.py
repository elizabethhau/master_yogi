from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS
from camera import VideoCamera
# import main
import os

# Set up Flask
app = Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")

# Set up Flask to bypass CORS at the front end
cors = CORS(app)

# keep track of the pose the user said
pose = None

@app.route('/')
def index():
  return render_template('index.html')

def generate(camera):
  counter = 0
  current_label = 'Unknown Pose'
  while True:
    frame, current_label = camera.get_frame(counter, current_label, pose)
    counter+=1
    yield(b'--frame\n'
    b'Content-Type: image/jpeng\n\n' + frame + b'\n\n')

@app.route('/video_feed')
def video_feed():
  return Response(generate(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/coach', methods=["POST"])
def coach():
  data = request.get_json()
  global pose
  pose = data['pose'].lower()
  print(pose)
  # TODO: call coach given pose and expect the message back
  # message = coach(pose, frame)
  messages = {'plank': 'keep your back straight', 'tree': 'make sure your foot is not on your knee', 'warrior': 'generic feedback for warrior 2'}

  return jsonify({'message': 'Lift your left arm'}) # hard coded for now, replace 'Lift your left arm' with the actual message for the user

# class VideoCamera(object):
#   def __init__(self) -> None:
#       self.video = cv2.VideoCapture(0)

#   def __del__(self):
#     self.video.release()

#   def get_frame(self):
#     ok, frame = self.video.read()
#     ok, jpeg = cv2.imencode('.jpg', frame)
#     return jpeg.tobytes()

# ## TESTING PURPOSES ONLY
# import numpy as np
#
# matrix = np.arange(36.).reshape((6, 6))
# rows, cols = matrix.shape
# #print(matrix)
# dictionary = [ {'x': j, 'y': i, 'value': matrix[j, i]} for j in range(rows) for i in range(cols) ]
# #print(dictionary)
#
# import json
# import sys
#
# #sys.stdout = open('declare.js', 'w') # Write 'w' output with the data into declare.js file
# #print(dictionary, file=open('declare.js', 'w'))
#
# # turn dictionary into json object
# jsonobj = json.dumps(dictionary)
#
# print("var jsonstr = '{}' ".format(jsonobj), file=open('declare.js', 'w'))
#
# ###############################

# Create the receiver API POST endpoint
@app.route('/receiver', methods=['POST'])
def postME():
    data = request.get_json()
    data = jsonify(data)
    return data

# Run the application
if __name__ == '__main__':
  app.run(host='127.0.0.1', port='8000', debug=True)