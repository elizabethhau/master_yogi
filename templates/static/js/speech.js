/*****************************************************************/
/*************** SPEECH GENERATION SETUP  ***********************/
/*****************************************************************/

// SPEECH SYNTHESIS SETUP
let voicesReady = false;
// let voiceIndices = [0]
let voiceIndices = [0, 7, 11, 17, 28, 32, 37, 41, 40, 49, 50, 51]
let coachIndex;
let coach;
let msg = new SpeechSynthesisUtterance();
const femaleNames = ['Olivia', 'Emma', 'Ava', 'Charlotte', 'Sophia', 'Amelia', 'Isabella', 'Mia', 'Emily', 'Lily'];
const maleNames = ['Liam', 'Noah', 'Oliver', 'William', 'James', 'Lucas', 'Adam', 'Robert', 'Max', 'Aaron'];
const genderNeutralNames = ['Morgan', 'Taylor', 'Alex', 'Blake'];
let prevMessage = '';

// This gets called on page load, excluding refreshes.
$(function() {
  console.log( "page is ready! selecting a coach for today" );
  coachIndex = voiceIndices[Math.floor(Math.random()*voiceIndices.length)]
  msg.voice =  window.speechSynthesis.getVoices()[coachIndex];
  coach = window.speechSynthesis.getVoices()[coachIndex].name;
  // coach = 'Alex';
  if (coach.includes('Google')) {
    if (coach.includes('Female')) {
      coach = femaleNames[Math.floor(Math.random()*femaleNames.length)]
    } else if(coach.includes('Male')) {
      coach = maleNames[Math.floor(Math.random()*maleNames.length)]
    } else {
      coach = genderNeutralNames[Math.floor(Math.random()*genderNeutralNames.length)]
    }
  }
  console.log(coach);
  generateSpeech('Hello! Welcome to Master Yogi!');
  setTimeout(() => generateSpeech('My name is ' + coach), 2000);
  setTimeout(() => generateSpeech('I will be helping you with your practice today.'), 5500);
  setTimeout(() => generateSpeech('To begin, say \"let\'s start yoga!"'), 9000);
  // setTimeout(() => generateSpeech(''), 2000);
});

window.speechSynthesis.onvoiceschanged = function () {
  voicesReady = true;
  console.log('voices ready is true')
  // Uncomment to see a list of voices
  //console.log("Choose a voice:\n" + window.speechSynthesis.getVoices().map(function(v,i) { return i + ": " + v.name; }).join("\n"));
};

const generateSpeech = function (message, callback) {
  // console.log("in generate speech, message is: ");
  // console.log(message);
  if (voicesReady) {
    console.log("VOICE IS READY");
    msg.text = message;
    msg.rate = 0.8;
    msg.volume = 1;
    // console.log(msg);
    if (typeof callback !== "undefined") {
      msg.onend = callback;
    }
    prevMessage = message;
    // if the current message is the same as the previous message, don't say it
    // if (!inCheckMode && prevMessage == message) {
    //   console.log('********* same message noticed, not going to repeat ***********');
    // } else {
    //   window.speechSynthesis.speak(msg);
    // }
    window.speechSynthesis.speak(msg);
  }
};
