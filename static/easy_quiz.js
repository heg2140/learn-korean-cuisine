let correctCount = 0;
let missedCount = 0;
let draggedItem = null;

// Handle drag start
document.querySelectorAll('.draggable').forEach(item => {
    item.addEventListener('dragstart', (e) => {
        draggedItem = e.target;
    });
});

// Handle drop zones
document.querySelectorAll('.dropzone').forEach(zone => {
    zone.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    zone.addEventListener('drop', (e) => {
        e.preventDefault();
        const correctAnswer = zone.dataset.answer;
        if (draggedItem.id === correctAnswer) {
            zone.appendChild(draggedItem);
            correctCount++;
            draggedItem.setAttribute("draggable", "false");
            draggedItem.style.cursor = "default";
        } else {
            missedCount++;
        }

        document.getElementById("correct").textContent = correctCount;
        document.getElementById("missed").textContent = missedCount;

        checkCompletion();
    });
});

// Timer setup
let timeLeft = 60;
const timerElement = document.getElementById("timer");

function updateTimer() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;

    if (timeLeft > 0) {
        timeLeft--;
    } else {
        clearInterval(timerInterval);
        endQuiz(); // Call function to handle end of quiz when time is up
    }
}

const timerInterval = setInterval(updateTimer, 1000);

// Function to handle end of quiz
function endQuiz() {
    missedCount = 5;
    document.getElementById("missed").textContent = missedCount;
    const time = document.getElementById("timer").textContent;
    localStorage.setItem("easyQuizTime", time);
    localStorage.setItem("easyQuizMissed", missedCount);
    window.location.href = "/quiz/easy/result";
}

// Check if quiz is complete
function checkCompletion() {
    if (correctCount === 5) {
        const time = document.getElementById("timer").textContent;
        localStorage.setItem("easyQuizTime", time);
        localStorage.setItem("easyQuizMissed", missedCount);
        setTimeout(() => {
            window.location.href = "/quiz/easy/result";
        }, 500);
    }
}
