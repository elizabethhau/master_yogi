
function loadPoseImage(poseString) {
    console.log('in load pose image')
    console.log(poseString)
    let displayString = "Pose: ";
    let imgSrc = "/static/images/";
    let result = false;
    poseString = poseString.toLowerCase();

    if (poseString.includes('tree')) {
        displayString += "Tree"
        imgSrc += "tree-pose.jpeg";
        result = true;
    }

    if (poseString.includes('warrior')) {
        displayString += "Warrior 2"
        imgSrc += "warrior-2.jpeg";
        result = true;
    }

    if (poseString.includes('plank') || poseString.includes('play')) {
        displayString += "Plank"
        imgSrc += "plank.jpeg";
        result = true;
    }
    if (result) {
        document.getElementById("pose_text").innerText = displayString;
        document.getElementById("pose_pic").src = imgSrc;
        document.getElementById("pose_pic").style.display = "inline";
    }
    return result
}

// only call losePoseImage once the page is fully loaded
// $(function() {
//     console.log( "page is ready!" );
    // loadPoseImage('plank');
// });
