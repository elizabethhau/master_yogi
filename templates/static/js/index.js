
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
        displayString += "Warrior2"
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
        console.log('about to fetch data')
        let data = {pose: displayString.toLowerCase()}
        console.log(data)
        fetch("http://127.0.0.1:8000/coach",
            {
                method: 'POST',
                headers: {
                    'Content-type': 'application/json',
                    'Accept': 'application/json'
                    // dataType: 'json'
                },
                body: JSON.stringify(data)})
            .then(res => {
                    if (res.ok) {
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
    return result
}

// only call losePoseImage once the page is fully loaded
// $(function() {
//     console.log( "page is ready!" );
    // loadPoseImage('plank');
// });
