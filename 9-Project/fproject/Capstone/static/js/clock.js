document.addEventListener("DOMContentLoaded", function () {
  let timerInterval;
  let timeLeft = 0;
  let isStudyTime = true;
  let cyclesLeft = 0;
  let soundPlayed = false;
  let breakSoundPlayed = false;

  const timerDisplay = document.getElementById("timer");
  const minutesDisplay = document.getElementById("minutes");
  const secondsDisplay = document.getElementById("seconds");
  const studyTimeMinutesInput = document.getElementById("studyTime");
  const studyTimeSecondsInput = document.getElementById("studyTimeSeconds");
  const breakTimeMinutesInput = document.getElementById("breakTime");
  const breakTimeSecondsInput = document.getElementById("breakTimeSeconds");
  const cyclesInput = document.getElementById("cycles");
  const startButton = document.getElementById("startTimer");
  const pauseButton = document.getElementById("pauseTimer");
  const resetButton = document.getElementById("resetTimer");

  // Cargar los sonidos
  const studyEndSound = new Audio(studyEndSoundPath);
  const breakEndSound = new Audio(breakEndSoundPath);

  function startTimer() {
    if (cyclesLeft === 0) {
      cyclesLeft = parseInt(cyclesInput.value);
    }
    if (isStudyTime) {
      const studyMinutes = parseInt(studyTimeMinutesInput.value) || 0;
      const studySeconds = parseInt(studyTimeSecondsInput.value) || 0;
      timeLeft = studyMinutes * 60 + studySeconds;
    } else {
      const breakMinutes = parseInt(breakTimeMinutesInput.value) || 0;
      const breakSeconds = parseInt(breakTimeSecondsInput.value) || 0;
      timeLeft = breakMinutes * 60 + breakSeconds;
    }
    soundPlayed = false;
    breakSoundPlayed = false;
    updateTimerDisplay();
    timerInterval = setInterval(updateTimer, 1000);
    startButton.style.display = "none";
    pauseButton.style.display = "inline-block";
    resetButton.style.display = "inline-block";
  }

  function pauseTimer() {
    clearInterval(timerInterval);
    startButton.style.display = "inline-block";
    pauseButton.style.display = "none";
  }

  function resetTimer() {
    clearInterval(timerInterval);
    timeLeft = 0;
    isStudyTime = true;
    cyclesLeft = 0;
    updateTimerDisplay();
    startButton.style.display = "inline-block";
    pauseButton.style.display = "none";
    resetButton.style.display = "none";
  }

  function updateTimer() {
    if (timeLeft <= 0) {
      clearInterval(timerInterval);
      if (isStudyTime) {
        alert("¡Tiempo de estudio terminado! Toma un descanso.");
      } else {
        alert("¡Tiempo de descanso terminado! Volvamos a estudiar.");
        cyclesLeft--;
        if (cyclesLeft <= 0) {
          resetTimer();
          return;
        }
      }
      isStudyTime = !isStudyTime;
      startTimer();
      return;
    }
    if (isStudyTime && timeLeft <= 5 && !soundPlayed) {
      studyEndSound.play();
      soundPlayed = true; 
    }

    if (!isStudyTime && timeLeft <= 1 && !breakSoundPlayed) {
      breakEndSound.play();
      breakSoundPlayed = true; 
    }

    timeLeft--;
    updateTimerDisplay();
  }

  function updateTimerDisplay() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    minutesDisplay.textContent = minutes < 10 ? `0${minutes}` : minutes;
    secondsDisplay.textContent = seconds < 10 ? `0${seconds}` : seconds;
  }

  startButton.addEventListener("click", startTimer);
  pauseButton.addEventListener("click", pauseTimer);
  resetButton.addEventListener("click", resetTimer);
});
