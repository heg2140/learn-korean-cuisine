let correctCount = 0;
let missedCount = 0;
let draggedItem = null;
const totalQuestions = 5;
let timeLeft = 60;

window.addEventListener("load", () => {
    const timerElement = document.getElementById("timer");

    // Setup draggable items
    document.querySelectorAll(".draggable").forEach(item => {
        item.addEventListener("dragstart", e => {
            draggedItem = item;
        });
    });

    // Setup dropzones
    document.querySelectorAll(".dropzone").forEach(zone => {
        zone.addEventListener("dragover", e => e.preventDefault());

        zone.addEventListener("drop", e => {
            e.preventDefault();
            if (!draggedItem) return;

            const dropMatchId = zone.dataset.matchId;
            const dragMatchId = draggedItem.dataset.matchId;

            if (dragMatchId === dropMatchId) {
                // Correct match
                zone.appendChild(draggedItem);
                draggedItem.setAttribute("draggable", "false");
                draggedItem.style.cursor = "default";

                zone.classList.add("matched");
                draggedItem.classList.add("matched");

                correctCount++;
            } else {
                // Incorrect match
                zone.classList.add("incorrect");
                draggedItem.classList.add("incorrect");

                missedCount++;

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
});

// Check if quiz is done
function checkCompletion() {
    if (correctCount === totalQuestions) {
        clearInterval(timerInterval);
        const timeTaken = document.getElementById("timer").textContent;
        window.location.href = `/quiz/hard/result?time=${encodeURIComponent(timeTaken)}&misses=${missedCount}`;
    }
}


// End quiz early
function endQuiz() {
    missedCount = 5;
    const timeTaken = document.getElementById("timer").textContent;
    window.location.href = `/quiz/hard/failed?time=${encodeURIComponent(timeTaken)}&misses=${missedCount}`;
}

// Play audio on click
function playCardAudio(button, event) {
    event.stopPropagation();
    const audio = button.closest(".card").querySelector("audio");
    if (audio) audio.play();
}
