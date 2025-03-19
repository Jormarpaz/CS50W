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
  const studyTimeInput = document.getElementById("studyTime");
  const breakTimeInput = document.getElementById("breakTime");
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
      timeLeft = parseInt(studyTimeInput.value) * 60;
    } else {
      timeLeft = parseInt(breakTimeInput.value) * 60;
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
      soundPlayed = true; // Marcar que el sonido ya se reprodujo
    }

    // Reproducir el sonido de descanso 2 segundos antes de que termine
    if (!isStudyTime && timeLeft <= 1 && !breakSoundPlayed) {
      breakEndSound.play();
      breakSoundPlayed = true; // Marcar que el sonido ya se reprodujo
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
