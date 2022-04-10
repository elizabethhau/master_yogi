import cv2
import mediapipe as mp

class VideoCamera(object):
  def __init__(self) -> None:
      self.video = cv2.VideoCapture(0)

  def __del__(self):
    self.video.release()

  def get_frame(self):
    ok, frame = self.video.read()
    ok, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes()