let correctCount = 0;
let missedCount = 0;
let draggedItem = null;
const totalQuestions = 5;
let timeLeft = 60;
const timerElement = document.getElementById("timer");

document.querySelectorAll('.draggable').forEach(item => {
    item.addEventListener('dragstart', (e) => {
        draggedItem = e.target;
    });
});

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

function updateTimer() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;

    if (timeLeft > 0) {
        timeLeft--;
    } else {
        clearInterval(timerInterval);
        endQuiz();
    }
}

const timerInterval = setInterval(updateTimer, 1000);

function endQuiz() {
    missedCount += totalQuestions - correctCount;
    const timeTaken = "1:00";
    window.location.href = `/quiz/hard/result?time=${encodeURIComponent(timeTaken)}&misses=${missedCount}`;
}

function checkCompletion() {
    if (correctCount === totalQuestions) {
        clearInterval(timerInterval);
        const timeTaken = document.getElementById("timer").textContent;
        window.location.href = `/quiz/hard/result?time=${encodeURIComponent(timeTaken)}&misses=${missedCount}`;
    }
}
