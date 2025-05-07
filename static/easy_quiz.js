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
            zone.classList.add('matched');
            draggedItem.classList.add('matched');
        } else {
            missedCount++;
            // Add red highlight
            zone.classList.add("incorrect");
            draggedItem.classList.add("incorrect", "shake");

            // Return the item to its original container
            const originalContainer = document.getElementById(`container-${draggedItem.id}`);
            originalContainer.appendChild(draggedItem);

            // Optional: disable drag temporarily to prevent spam-drop
            draggedItem.setAttribute("draggable", "false");

            // Remove highlight after short delay
            setTimeout(() => {
                zone.classList.remove("incorrect");
                draggedItem.classList.remove("incorrect", "shake");
                draggedItem.setAttribute("draggable", "true");
            }, 500);
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

    // Save to localStorage (optional)
    localStorage.setItem("easyQuizTime", time);
    localStorage.setItem("easyQuizMissed", missedCount);

    // Redirect with query parameters
    window.location.href = `/quiz/easy/failed?time=${encodeURIComponent(time)}&misses=${missedCount}`;
}

function checkCompletion() {
    if (correctCount === 5) {
        const time = document.getElementById("timer").textContent;

        // Save to localStorage (optional)
        localStorage.setItem("easyQuizTime", time);
        localStorage.setItem("easyQuizMissed", missedCount);

        // Delay before redirect
        setTimeout(() => {
            window.location.href = `/quiz/easy/result?time=${encodeURIComponent(time)}&misses=${missedCount}`;
        }, 500);
    }
}
