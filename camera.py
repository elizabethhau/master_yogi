import cv2
import mediapipe as mp
import math
import numpy as np
from time import time
import matplotlib.pyplot as plt
import pandas as pd
import json # For communicating between Python and Javascript/HTML

class VideoCamera(object):
  def __init__(self) -> None:
    self.video = cv2.VideoCapture(0)
    # Initializing mediapipe pose class
    self.mp_pose = mp.solutions.pose
    # Setting up the Pose function
    self.pose = self.mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)
    # Initializing mediapipe drawing class, useful for annotation
    self.mp_drawing = mp.solutions.drawing_utils
    # Set up pose function for video
    self.pose_video = self.mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)


  def __del__(self):
    self.video.release()

  def detect_pose(self, image, pose, display=True):
    '''
		This function performs pose detection on an image.
		Args:
				image: The input image with a prominent person whose pose landmarks needs to be detected.
				pose: The pose setup function required to perform the pose detection.
				display: A boolean value that is if set to true the function displays the original input image, the resultant image,
								 and the pose landmarks in 3D plot and returns nothing.
		Returns:
				output_image: The input image with the detected pose landmarks drawn.
				landmarks: A list of detected landmarks converted into their original scale.
		'''
    # Create a copy of the input image
    output_image = image.copy()

    # Convert the image from BGR into RGB format
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform the pose detection
    results = pose.process(image_rgb)

    # Retrieve the height and width of the input image
    height, width, _ = image.shape

    # Initialize a list to store the detected landmarks
    landmarks = []

    # Check if any landmarks are detected
    if results.pose_landmarks:
      # draw pose landmarks on the output image
      self.mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                     connections=self.mp_pose.POSE_CONNECTIONS,
                                     landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(255, 0, 0),
                                                                                       thickness=5,
                                                                                       circle_radius=5),
                                     connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 128, 0),
                                                                                         thickness=8,
                                                                                         circle_radius=2))

      # iterate over the detected landmarks
      for landmark in results.pose_landmarks.landmark:
        # append the landmark into the list
        landmarks.append(
          (round(landmark.x * width, 2), round(landmark.y * height, 2), round(landmark.z * width, 2)))

    # check if the original input image and the resultant image are specified to be displayed
    if display:
      # display the original input image and the resultant image
      plt.figure(figsize=[22, 22])
      plt.subplot(121)
      plt.imshow(image[:, :, ::-1])
      plt.title("Original Image")
      plt.axis('off')
      plt.subplot(122)
      plt.imshow(output_image[:, :, ::-1])
      plt.title("Output Image")
      plt.axis('off')

      # also plot the pose landmarks in 3D
      self.mp_drawing.plot_landmarks(results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

    return output_image, landmarks

  def calculate_angle(self, landmark1, landmark2, landmark3):
    '''
					This function calculates angle between three different landmarks.
					Args:
							landmark1: The first landmark containing the x,y and z coordinates.
							landmark2: The second landmark containing the x,y and z coordinates.
							landmark3: The third landmark containing the x,y and z coordinates.
					Returns:
							angle: The calculated angle between the three landmarks.
				'''
    # Get the required landmarks coordinates
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    # calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))

    # check if the angle is less than zero
    if angle < 0:
      # add 360 degrees to the found angle
      angle += 360
    return angle

  def coach_pose(self, landmarks, output_image, database, counter, display=False, pose='plank', user_level='beginner'):
    '''
				This function classifies yoga poses depending upon the angles of various body joints.
				Args:
						landmarks: A list of detected landmarks of the person whose pose needs to be classified.
						output_image: A image of the person with the detected pose landmarks drawn.
						display: A boolean value that is if set to true the function displays the resultant image with the pose label
						written on it and returns nothing.
				Returns:
						output_image: The image with the detected pose landmarks drawn and pose label written.
						label: The classified pose label of the person in the output_image.

				'''
    # Initializing the label of the pose. It is not known at this stage.
    label = str('Unknown Pose')

    # If it is the first iteration based on the counter ... then upload the database of poses and just return the frame, unkown pose etc.
    # I feel like we
    #if counter == 0:
      #global database
      #database = pd.read_csv(r"yoga_poses_csvs_out_AnglesExtracted.csv")
      #correction_message = str('Let us do yoga') #+ str(pose) ##so this would be a message that kicks it off only works if we reset the counter every time the user says a new pose
      ##testing pose filter to confirm it works ... print(database[database['Pose']==pose])

      #return output_image, label, correction_message

    ##Now the data base is uploaded into the app ... filter on pose and feature
    ##Example query database[database['Pose'] == pose] ... where pose is fed in by user, need to convert to one word lower case ie. downdog, plank


    # Specify the color (Red) with which the label will be written on the image
    color = (0, 0, 255)

    # Calculate the required angles.
    # ----------------------------------------------------------------------------------------------------------------

    # Get the angle between the left shoulder, elbow and wrist points.
    Left_Elbow_Angle = self.calculate_angle(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                            landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value])

    # Get the angle between the right shoulder, elbow and wrist points.
    Right_Elbow_Angle = self.calculate_angle(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                             landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                             landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value])
    # Get the angle between the left elbow, shoulder and hip points.
    Left_Shoulder_Angle = self.calculate_angle(landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                               landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                               landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value])

    # Get the angle between the right hip, shoulder and elbow points.
    Right_Shoulder_Angle = self.calculate_angle(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                                landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                                landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value])

    # Get the angle between the left hip, knee and ankle points.
    Left_Knee_Angle = self.calculate_angle(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value],
                                           landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value],
                                           landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value])

    # Get the angle between the right hip, knee and ankle points
    Right_Knee_Angle = self.calculate_angle(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                            landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                            landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value])

    Torso_Alignment = self.calculate_angle(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                            landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                            landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value])

    current_pose = pd.Series([Left_Elbow_Angle, Right_Elbow_Angle, Left_Shoulder_Angle, Right_Shoulder_Angle, Left_Knee_Angle, Right_Knee_Angle,
                              Torso_Alignment], index = ['Left Elbow Angle', 'Right Elbow Angle', 'Left Shoulder Angle', 'Right Shoulder Angle', 'Left Knee Angle',
                                                         'Right Knee Angle', 'Torso Alignment'])
    # ---------------------------------------------------------------------------------------------------------------- #
    ##Get the representative pose angles from our database ...
    pose_examples = database[database['Pose'] == pose]
    #print(pose_examples)
    ##Get the standard deviation of each feature ...

    ##drop the non-numeric columns to prevent a type erro
    pose_examples = pose_examples.drop('Image_Name', axis=1)
    pose_examples = pose_examples.drop('Pose', axis=1)

    stdevs = pose_examples.std().sort_values() ##this sorts the features based off std.
    #print(stdevs)
    avg_features = pose_examples.mean()
    #print(avg_features)



    for item in stdevs.iteritems():
      ##check each feature prioritized by standard deviation of the feature, low standard deviation means important to the pose
      #print(item)

      ##figure out which feature it is
      feature = item[0]
      target_dev = item[1]
      #print(feature)

      ##check that feature against the realtime pose...
      ##add if statement
      if user_level == 'beginner':
        target_dev = 1.5*target_dev
      # if user_level == 'advanced':
      #   print("advanced!!")

      if (current_pose[feature] < avg_features[feature] - target_dev) or (current_pose[feature] > avg_features[feature] + target_dev):
        if feature == 'Torso Alginment':
        #print('Align your torso')
          correction_message = 'Align your torso'
          return output_image, label, correction_message
        if feature == 'Left Elbow Angle':
          #print('Straighten Your Right Arm') ##figured out these are reversed so coding the correction opposite
          correction_message = 'Straighten Your Right Arm'
          return output_image, label, correction_message
        if feature == 'Right Elbow Angle':
          #print('Straighten Your Left Arm')
          correction_message = 'Straighten Your Left Arm'
          return output_image, label, correction_message
        if feature == 'Left Shoulder Angle':
          print('Increase the distance between your right arm and torso')
          correction_message = 'Increase the distance between your right arm and torso'
          return output_image, label, correction_message
        if feature == 'Right Shoulder Angle':
          #print('Increase the distance between your left arm and torso')
          correction_message = 'Increase the distance between your left arm and torso'
          return output_image, label, correction_message
        if feature == 'Right Knee Angle':
          #print('Straighten your left leg')
          correction_message = 'Straighten your left leg'
          return output_image, label, correction_message

    label = str(pose)

    #if right_elbow_angle < 165 or right_elbow_angle > 195:
      #print('Extend your right arm straight')

      #print('Can you do that?') ##could we get the system to wait for a response here from the user?


    ##Original Implementation ....

    # Check if it is the warrior II pose or the T pose.
    # As for both of them, both arms should be straight and shoulders should be at the specific angle.
    # ----------------------------------------------------------------------------------------------------------------
    # Check if the both arms are straight.
    #if left_elbow_angle > 165 and left_elbow_angle < 195 and right_elbow_angle > 165 and right_elbow_angle < 195:

      # Check if shoulders are at the required angle.
      #if left_shoulder_angle > 80 and left_shoulder_angle < 110 and right_shoulder_angle > 80 and right_shoulder_angle < 110:

        # Check if it is the warrior II pose.
        # ----------------------------------------------------------------------------------------------------------------

        # Check if one leg is straight.
        #if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:

          # Check if the other leg is bended at the required angle.
          #if left_knee_angle > 90 and left_knee_angle < 120 or right_knee_angle > 90 and right_knee_angle < 120:
            # Specify the label of the pose that is Warrior II pose.
            #label = 'Warrior II Pose'

          # ----------------------------------------------------------------------------------------------------------------

        # Check if it is the T pose.
        # ----------------------------------------------------------------------------------------------------------------

        # Check if both legs are straight
        #if left_knee_angle > 160 and left_knee_angle < 195 and right_knee_angle > 160 and right_knee_angle < 195:
          # Specify the label of the pose that is tree pose.
          #label = 'T Pose'

    # ----------------------------------------------------------------------------------------------------------------

    # Check if it is the tree pose.
    # ----------------------------------------------------------------------------------------------------------------

    # Check if one leg is straight
    #if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:

      # Check if the other leg is bended at the required angle.
      #if left_knee_angle > 315 and left_knee_angle < 335 or right_knee_angle > 25 and right_knee_angle < 45:
        # Specify the label of the pose that is tree pose.
        #label = 'Tree Pose'

    # ----------------------------------------------------------------------------------------------------------------

    # Check if the pose is classified successfully
    #if label != str('Unknown Pose'):
      # Update the color (to green) with which the label will be written on the image.
    color = (0, 255, 0)

    # Write the label on the output image.
    cv2.putText(output_image, label, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

    success_message = str('Good job on this pose')

    # Return the output image and the classified label.
    return output_image, label, success_message

  def get_frame(self, counter, current_label, database, pose=None, user_level='beginner'):
    ok, frame = self.video.read()

    message_to_user = None

    # flip the frame horizontally for natural (selfie-view) visualization
    frame = cv2.flip(frame, 1)

    # get the width and height of the frame
    frame_height, frame_width, _ = frame.shape

    #resize the frame while keeping the aspect ratio
    frame = cv2.resize(frame, (int(frame_width * (640/frame_height)), 640))

    # Perform pose landmark detection
    frame, landmarks = self.detect_pose(frame, self.pose_video, display=False)

    # chck if landmarks are detected
    if landmarks:
      # Look at the posture and provide coaching feedback.

      ##I think this is where we can change the sampling rate with a counter ... we only classify and coach every XX iterations
      ##How can I get the goal pose here...need to get this from the JS to know what the user is trying to do and then coach the pose...

      if counter % 50 == 0 and pose != None:  ##we can change the sampling rate for coaching without interupting the video feed.
        #print(counter)

          ##send request from python to java script ... asking for user input

        frame, current_label, message_to_user = self.coach_pose(landmarks, frame, database, counter=counter, display=False, pose=pose, user_level=user_level) ##need to get the pose the user is saying here
        #print(message_to_user)
        ##send a request JS to output message to the user ...




    #Write the label on the frame and pass it back
    if current_label != 'Unknown Pose':
      frame = cv2.putText(frame, current_label, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    else:
      frame = cv2.putText(frame, current_label, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)


    ok, jpeg = cv2.imencode('.jpg', frame)


    return jpeg.tobytes(), current_label, message_to_user

