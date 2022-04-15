// SPEECH SYNTHESIS SETUP
let voicesReady = false;
window.speechSynthesis.onvoiceschanged = function () {
  voicesReady = true;
  console.log('voices ready is true')
  // Uncomment to see a list of voices
  //console.log("Choose a voice:\n" + window.speechSynthesis.getVoices().map(function(v,i) { return i + ": " + v.name; }).join("\n"));
};

const generateSpeech = function (message, callback) {
  console.log("in generate speech, message is: ");
  console.log(message);
  if (voicesReady) {
    console.log("VOICE IS READY");
    var msg = new SpeechSynthesisUtterance();
    msg.voice = window.speechSynthesis.getVoices()[0];
    // console.log(window.speechSynthesis.getVoices());
    msg.text = message;
    // msg.rate = 0.2;
    msg.rate = 0.8;
    msg.volume = 1;
    // console.log(msg);
    if (typeof callback !== "undefined") {
      msg.onend = callback;
    }
    speechSynthesis.speak(msg);
  }
};
