let correctCount = 0;
let missedCount = 0;
let draggedItem = null;
const totalQuestions = 5;
let timeLeft = 60;
const timerElement = document.getElementById("timer");

document.addEventListener('DOMContentLoaded', () => {
    // Drag start handler
    document.querySelectorAll('.draggable').forEach(item => {
        item.addEventListener('dragstart', (e) => {
            draggedItem = item;
        });
    });

    // Drop logic
    document.querySelectorAll('.dropzone').forEach(zone => {
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
        });

        zone.addEventListener('drop', (e) => {
            e.preventDefault();

            const correctAnswer = zone.dataset.matchId;
            if (!draggedItem) return;

            if (draggedItem.dataset.matchId === correctAnswer) {
                // ✅ Correct match
                zone.appendChild(draggedItem);
                correctCount++;

                draggedItem.setAttribute("draggable", "false");
                draggedItem.style.cursor = "default";

                zone.classList.add("matched");
                draggedItem.classList.add("matched");
            } else {
                // ❌ Incorrect match
                missedCount++;

                zone.classList.add("incorrect");
                draggedItem.classList.add("incorrect");

                setTimeout(() => {
                    zone.classList.remove("incorrect");
                    draggedItem.classList.remove("incorrect");
                }, 500);
            }

            document.getElementById("correct").textContent = correctCount;
            document.getElementById("missed").textContent = missedCount;

            checkCompletion();
        });
    });
});

// Timer logic
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

// Redirect when time is up
function endQuiz() {
    missedCount += totalQuestions - correctCount;
    const timeTaken = document.getElementById("timer").textContent;
    window.location.href = `/quiz/hard/result?time=${encodeURIComponent(timeTaken)}&misses=${missedCount}`;
}

// Redirect when quiz is complete
function checkCompletion() {
    if (correctCount === totalQuestions) {
        clearInterval(timerInterval);
        const timeTaken = document.getElementById("timer").textContent;
        window.location.href = `/quiz/hard/result?time=${encodeURIComponent(timeTaken)}&misses=${missedCount}`;
    }
}

// Play audio from card
function playCardAudio(button, event) {
    event.stopPropagation();
    const audio = button.closest('.card').querySelector('audio');
    if (audio) {
        audio.play();
    }
}
