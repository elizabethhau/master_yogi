# Master Yogi
6.835 Final Project, Spring 2022

## Project Description
Our application coaches beginners through a series of yoga poses to help them improve their posture. The coaching is generalizable to any individual and body-shape agnostic. 

Our team used OpenCV2 for real-time 3D pose detection and pose classification. We developed a friendly UI for users to interact with and get personalized feedback.

## Installation
Run the following command to install the necessary dependencies:
`pip install -r requirements.txt`

Alternatively, you can manually install the versions in your virtual environment:
1. `pip install opencv-python==4.5.5.64`
2. `pip install mediapipe==0.8.9.1`
3. `pip install matplotlib==3.5.1`
4. `pip install flask==2.1.1`

## Usage
Run the application using the command `python app.py` in the directory where `app.py` lives. 

Then, open local host on your favorite browser: `http://0.0.0.0:8000/`. Follow the instructions on the UI and have fun! :) 

## Potential Errors
You may encounter some errors, so we've compiled a list of resolutions here:

1. Microphone/camera is not working on Google Chrome for insecure origins: Navigate to `chrome://settings/content/sound` and manually adding `http://127.0.0.1:8000/` to a list of sites "Allowed to play sound" (https://medium.com/@Carmichaelize/enabling-the-microphone-camera-in-chrome-for-local-unsecure-origins-9c90c3149339)

## Authors
LGO 22s Elizabeth Hau, Andrew Tindall, and Sravani Yajamanam Kidambi.

## References
- [Real-Time 3D Pose Detection and Classification](https://bleedai.com/introduction-to-pose-detection-and-basic-pose-classification/)