var hasLoadedPose = false;
var inCheckMode = false;
let poseSelected = '';

function everyTime() {
    console.log('each 1 second...');
}

var myInterval = setInterval(everyTime, 1000);

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
            generateSpeech("Ok, entering check mode. I will provide adjustments periodically as you practice this pose");
            inCheckMode = true;
            // console.log('set check mode to true')
            // console.log('check mode is' + inCheckMode);
        }, 3000)
    }

    return result
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
