let saidStartYoga = false;
let level_set = false;
let user_level;
let hasLoadedPose = false;
let poseSelected = '';
let inCheckMode = false;

function everyTime() {
    console.log('each 1 second...');
}

var myInterval = setInterval(everyTime, 1000);

function setStartYoga(transcript) {
    transcript = transcript.toLowerCase();
    setTimeout(() => {
        if (transcript.includes('yoga')) {
        saidStartYoga = true;
        generateSpeech('Great! I can coach you as a beginner or advanced yogi. Please tell me your skill level');
        return true;
    }
    }, 2000);

    return false;
}

function loadPoseImage(poseString) {
    console.log('in load pose image')
    console.log(poseString)

    let displayString = "Pose: ";
    let imgSrc = "/static/images/";
    let result = false;
    poseString = poseString.toLowerCase();

    if (poseString.includes('tree')) {
        displayString += "Tree"
        poseSelected = "tree";
        imgSrc += "tree-pose.jpeg";
        result = true;
    }

    if (poseString.includes('warrior')) {
        displayString += "Warrior2";
        poseSelected = "warrior2";
        imgSrc += "warrior-2.jpeg";
        result = true;
    }

    if (poseString.includes('plank') || poseString.includes('play')) {
        displayString += "Plank"
        poseSelected = "plank";
        imgSrc += "plank.jpeg";
        result = true;
    }
    if (result) {
        hasLoadedPose = true;
        document.getElementById("pose_text").innerText = displayString;
        document.getElementById("pose_pic").src = imgSrc;
        document.getElementById("pose_pic").style.display = "inline";
        setTimeout(() => {
            generateSpeech("Ok, please get into the pose. I will provide adjustments periodically as you practice this pose");
            inCheckMode = true;
            // console.log('set check mode to true')
            // console.log('check mode is' + inCheckMode);
        }, 3000)
    }

    return result
}

function set_level_function(level) {
    let result = false;
    level_string = level.toLowerCase();

    if (level_string.includes('advanced') || level_string.includes('advance')) {
        user_level = 'advanced';
        result = true;
    }

    if (level_string.includes('beginner') || level_string.includes('begin')) {
        user_level = 'beginner';
        result = true;
    }

    let success = false;
    if (result) {
        fetch("http://127.0.0.1:8000/user_level",
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
                // dataType: 'json'
            },
            body: JSON.stringify({user_level: user_level})})
        .then(res => {
                if (res.ok) {
                    level_set = true;
                    success = true;
                    return success;
                }
                return false;
                // alert('something went wrong')
            })
        .catch(err => console.error(err))
        generateSpeech('Ok, the level has been set to ' + user_level + '. I can currently coach the three poses listed on the screen. I am in the process of learning more poses. Let me know which pose you would like to practice');
         // When you are ready for feedback, tell me the pose you selected and say "check"
    }
    return success
}

function coachPose() {
    // console.log('about to fetch data')
    // console.log('in coach pose');
    // console.log('has loaded pose');
    // console.log(hasLoadedPose);
    // console.log('in check mode');
    // console.log(inCheckMode);
    let success = false;
    if (hasLoadedPose && inCheckMode) {
        fetch("http://127.0.0.1:8000/coach",
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
                // dataType: 'json'
            },
            body: JSON.stringify({pose: poseSelected})})
        .then(res => {
                if (res.ok) {
                    success = true;
                    return res.json()
                }
                alert('something went wrong')
            })
        .then(jsonResponse => {
                let message = jsonResponse.message
                generateSpeech(jsonResponse.message)
                document.getElementById("feedback").innerText = message;
                console.log(message)
            })
        .catch(err => console.error(err))
    }
    return success

}

var checkingpose = setInterval(coachPose
  , 10000);

// only call losePoseImage once the page is fully loaded
// $(function() {
//     console.log( "page is ready!" );
    // loadPoseImage('plank');
// });
