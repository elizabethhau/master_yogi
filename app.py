from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS
from camera import VideoCamera
import pandas as pd
import os
import aioflask
import asyncio

# Set up Flask
app = Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")

# Set up Flask to bypass CORS at the front end
cors = CORS(app)

# Build the pose database here instead of inside the camera funtion...
global database
global message_to_user
global user_level
user_level = str('beginner')
database = pd.read_csv(r"yoga_poses_csvs_out_AnglesExtracted.csv")
message_to_user = str('Let\'s do yoga')

pose = None

@app.route('/')
def index():
  return render_template('index.html')

def generate(camera):
  counter = 0
  current_label = 'Unknown Pose'


  global message_to_user
  global database
  global user_level

  while True:
    frame, current_label, message = camera.get_frame(counter, current_label, database, pose, user_level) # User level will get passed to camera for every frame
    if message != None:
      message_to_user = message

    counter+=1
    yield(b'--frame\n'
    b'Content-Type: image/jpeng\n\n' + frame + b'\n\n')

@app.route('/video_feed')
def video_feed():
  return Response(generate(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/coach', methods=["POST"])
async def coach():
  data = request.get_json()
  print(data)
  global pose
  global message_to_user

  pose = data['pose'].lower()
  print(pose)
  await asyncio.sleep(2)
  print(str('Coach says: '), message_to_user)

  return jsonify({'message': message_to_user})

# User level gets updated to whatever the user says
@app.route('/user_level', methods=["POST"])
async def user_level():
  data = request.get_json()
  print(data)
  global user_level
  user_level = data['user_level'].lower()
  print(user_level)
  return jsonify({'user_level': user_level})

# Run the application
if __name__ == '__main__':
  app.run(host='127.0.0.1', port='8000', debug=True)