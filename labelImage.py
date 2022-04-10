import math
import cv2
import numpy as np
from time import time
import mediapipe as mp
import matplotlib.pyplot as plt

def label_image(input_image_path):
    #Read an image from the specified path.
    sample_img = cv2.imread(input_image_path)

    # Specify a size of the figure.
    plt.figure(figsize=[10, 10])

    # Display the sample image, also convert BGR to RGB for display.
    plt.title("Sample Image");
    plt.axis('off');
    plt.imshow(sample_img[:, :, ::-1]);
    plt.show()

    # Perform pose detection after converting the image into RGB format.
    results = pose.process(cv2.cvtColor(sample_img, cv2.COLOR_BGR2RGB))

    # Check if any landmarks are found.
    if results.pose_landmarks:

        # Iterate two times as we only want to display first two landmarks.
        for i in range(2):
            # Display the found normalized landmarks.
            print(f'{mp_pose.PoseLandmark(i).name}:\n{results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value]}')

        # Retrieve the height and width of the sample image.
        image_height, image_width, _ = sample_img.shape

        # Check if any landmarks are found.
        if results.pose_landmarks:

        # Iterate two times as we only want to display first two landmark.
            for i in range(2):
                # Display the found landmarks after converting them into their original scale.
                print(f'{mp_pose.PoseLandmark(i).name}:')
                print(f'x: {results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].x * image_width}')
                print(f'y: {results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].y * image_height}')
                print(f'z: {results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].z * image_width}')
                print(f'visibility: {results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].visibility}\n')

        # Retrieve the height and width of the sample image.
    image_height, image_width, _ = sample_img.shape

    # Check if any landmarks are found.
    if results.pose_landmarks:

    # Iterate two times as we only want to display first two landmark.
        for i in range(2):
            # Display the found landmarks after converting them into their original scale.
            print(f'{mp_pose.PoseLandmark(i).name}:')
            print(f'x: {results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].x * image_width}')
            print(f'y: {results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].y * image_height}')
            print(f'z: {results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].z * image_width}')
            print(f'visibility: {results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].visibility}\n')


    img_copy = sample_img.copy()

    # Check if any landmarks are found.
    if results.pose_landmarks:
        # Draw Pose landmarks on the sample image.
        mp_drawing.draw_landmarks(image=img_copy, landmark_list=results.pose_landmarks,
                              connections=mp_pose.POSE_CONNECTIONS,
                              landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255,0,0), thickness=5, circle_radius=5),
                              connection_drawing_spec=mp_drawing.DrawingSpec(color=(0,128,0), thickness=8, circle_radius=2))

        # Specify a size of the figure.
        fig = plt.figure(figsize=[10, 10])

        # Display the output image with the landmarks drawn, also convert BGR to RGB for display.
        plt.title("Output");
        plt.axis('off');
        plt.imshow(img_copy[:, :, ::-1]);
        plt.show()


    # Plot Pose landmarks in 3D.
    mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)