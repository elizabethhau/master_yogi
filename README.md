# Master Yogi
6.835 Final Project, Spring 2022

## Project Description
Our application coaches beginners through a series of yoga poses to help them improve their posture. The coaching is generalizable to any individual and body-shape agnostic. 

Our team used OpenCV2 and Google's mediapipe for real-time 3D pose detection and pose classification. We developed a friendly UI for users to interact with and get personalized feedback.

## Installation
Master Yogi has been developed and tested on Python 3.7, so earlier versions may or may not work.

To install the necessary dependencies, run the command:
`pip install -r requirements.txt`

Alternatively, you can manually install the versions in your virtual environment (MacOS):
1. `pip install opencv-python==4.5.5.64`
2. `pip install mediapipe==0.8.9.1`
3. `pip install matplotlib==3.5.1`
4. `pip install flask==2.1.1`
5. `pip install Flask-Cors==3.0.10`
6. `pip install aioflask`
7. `pip install asyncio`

## Usage
Run the application using the command `python app.py` in the directory where `app.py` lives. 

Then, open local host on your favorite browser: `http://127.0.0.1:8000/`. Follow the instructions on the UI and have fun! :) 

## File Descriptions
### Front-end:
All front-end code files live in `/templates/static/js` folder, which communicates to the back-end through Flask:
* `setupSpeech.js`: handles "speech-to-text" processing of spoken speech
* `speech.js`: handles "text-to-speech" speech generation
* `index.js`: handles the rest of the javascript functionality such as setting the user's level (beginner or advanced), loading up the image corresponding to the pose selected by the user, providing feedback, "skip" functionality, etc.

### Back-end:
Our back-end is built with python's Flask. Back-end files include:
* `app.py`: main entry point for the application. Defines endpoints that communicate with the front-end JavaScript. Endpoints include:
  * `index`: points to `index.html` as the front-end template to load up for the application
  * `video_feed`: reads frames from the computer's video camera and displays it on the webpage
  * `coach`: Given the pose selected by the user (from JS), fetch feedback for the user and pass it back to the front-end
  * `user_level`: Given the user selected level, set the system to either provide stricter feedback (advanced users) or more lenient feedback (to beginner users)

* `camera.py`: Defines a Camera object that processes video frames and performs pose detection, classification, and feedback recommendation based on the provided user level, which is currently either "beginner" or "advanced." The advanced level will be more strict about the relative angles between the joints. 

### Data:
We have included two files that we used as training data in the repository as well:
* `yoga_poses_csvs_out_AnglesExtracted.csv`: This file contains the training data extracted from images we used to train our system. The data contains angles between detected body joints 
* `yoga_poses_csvs_out_basic (4).csv`

## Potential Errors
You may encounter some errors, so we've compiled a list of resolutions here:

1. Microphone/camera is not working on Google Chrome for insecure origins: Navigate to `chrome://settings/content/sound` and manually adding `http://127.0.0.1:8000/` to a list of sites "Allowed to play sound" (https://medium.com/@Carmichaelize/enabling-the-microphone-camera-in-chrome-for-local-unsecure-origins-9c90c3149339)

## Authors
LGO 22s Elizabeth Hau, Andrew Tindall, and Sravani Yajamanam Kidambi.

## References
- [Real-Time 3D Pose Detection and Classification](https://bleedai.com/introduction-to-pose-detection-and-basic-pose-classification/)