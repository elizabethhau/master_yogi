
function loadPoseImage(poseString) {
    var displayString = "Pose: ";
    var imgSrc = "/static/images/";

    if (poseString.toLowerCase().includes('tree')) {
        displayString += "Tree"
        imgSrc += "tree-pose.jpeg";
    }

    if (poseString.toLowerCase().includes('warrior two')) {
        displayString += "Warrior 2"
        imgSrc += "warrior-2.jpeg";
    }

    if (poseString.toLowerCase().includes('plank')) {
        displayString += "Plank"
        imgSrc += "plank.jpeg";
    }
    document.getElementById("pose_text").innerText = displayString;
    document.getElementById("pose_pic").src = imgSrc;
}

// only call losePoseImage once the page is fully loaded
$(function() {
    console.log( "ready!" );
    loadPoseImage('plank');
});
