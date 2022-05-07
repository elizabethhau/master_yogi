/*****************************************************************/
/******** SPEECH RECOGNITION SETUP YOU CAN IGNORE ****************/
/*****************************************************************/

// processSpeech(transcript)
//  Is called anytime speech is recognized by the Web Speech API
// Input:
//    transcript, a string of possibly multiple words that were recognized
// Output:
//    processed, a boolean indicating whether the system reacted to the speech or not


const processSpeech = function (transcript) {
  // console.log('check mode is');
  // console.log(inCheckMode);
  // console.log('in process speech')
  // console.log('transcript is')
  // console.log(transcript)
  transcript = transcript.toLowerCase();
  // Helper function to detect if any commands appear in a string
  const userSaid = function (str, commands) {
    for (var i = 0; i < commands.length; i++) {
      if (str.indexOf(commands[i]) > -1) return true;
    }
    return false;
  };

  var processed = false;

  if (!saidStartYoga) {
    processed = setStartYoga(transcript);
  } else if (!level_set) {
    processed = set_level_function(transcript)
  } //else if (transcript.includes('no')) {
    //processed = endPractice(transcript);
  //}
  else if (!hasLoadedPose) {
    processed = loadPoseImage(transcript);
  // } else if (transcript.includes('skip')) {
  } else if (coachFetchedCount > 2) {
    processed = skip(transcript);
  }

  return processed;
};

let debouncedProcessSpeech = _.debounce(processSpeech, 500);

let recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;
recognition.onresult = function(event) {
  // Build the interim transcript, so we can process speech faster
  let transcript = '';
  let hasFinal = false;
  for (var i = event.resultIndex; i < event.results.length; ++i) {
    if (event.results[i].isFinal)
      hasFinal = true;
    else
      transcript += event.results[i][0].transcript;
  }

  // if (DEBUGSPEECH) {
    if (hasFinal) {
      // console.log("SPEECH DEBUG: ready");
      document.getElementById('speech').innerText = "System ready: listening..."
    }
      // otherFeedback.setContent("SPEECH DEBUG: ready");
    else {
      // console.log("SPEECH DEBUG: " + transcript);
      document.getElementById('speech').innerText = "You said: " + transcript;
    }

      // otherFeedback.setContent("SPEECH DEBUG: " + transcript);
  // }

  let processed = debouncedProcessSpeech(transcript);

  // If we reacted to speech, kill recognition and restart
  if (processed) {
    recognition.stop();
  }
};
// Restart recognition if it has stopped
recognition.onend = function(event) {
  setTimeout(function() {
    // if (DEBUGSPEECH)
    // otherFeedback.setContent("SPEECH DEBUG: ready");
    console.log('SPEECH DEBUG: ready')
    recognition.start();
  }, 1000);
};

recognition.start();
/*****************************************************************/
/******** END OF SPEECH RECOG SETUP ******************************/
/*****************************************************************/

