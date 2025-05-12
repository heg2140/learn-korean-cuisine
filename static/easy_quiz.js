let correctCount = 0;
let missedCount = 0;
let draggedItem = null;
const totalQuestions = document.querySelectorAll('.dropzone').length;

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
        const isCorrect = draggedItem.id === correctAnswer;
    
        // ✅ Log attempt
        fetch("/quiz/easy/log-answer", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            match_id: draggedItem.id,
            source_type: "label",
            target_type: "dropzone",
            is_correct: isCorrect
          })
        });
    
        if (isCorrect) {
            zone.appendChild(draggedItem);
            correctCount++;
            draggedItem.setAttribute("draggable", "false");
            draggedItem.style.cursor = "default";
            zone.classList.add('matched');
            draggedItem.classList.add('matched');
        } else {
            missedCount++;
            zone.classList.add("incorrect");
            draggedItem.classList.add("incorrect", "shake");
    
            const originalContainer = document.getElementById(`container-${draggedItem.id}`);
            if (originalContainer) {
                originalContainer.appendChild(draggedItem);
            }
    
            draggedItem.setAttribute("draggable", "false");
    
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
    const timeTaken = document.getElementById("timer").textContent;
  
    fetch("/quiz/easy/store-result", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        outcome: "failed",
        time: timeTaken,
        misses: missedCount,
        matches: correctCount
      })
    })
    .catch(err => console.error("Easy quiz result logging failed:", err))
    .finally(() => {
      window.location.href = `/quiz/easy/failed?time=${encodeURIComponent(timeTaken)}&misses=${missedCount}`;
    });
  }

function checkCompletion() {
    if (correctCount === totalQuestions) {
      clearInterval(timerInterval);
      const timeTaken = document.getElementById("timer").textContent;
  
      fetch("/quiz/easy/store-result", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          outcome: "won",
          time: timeTaken,
          misses: missedCount,
          matches: correctCount
        })
      })
      .catch(err => console.error("Easy quiz result logging failed:", err))
      .finally(() => {
        window.location.href = `/quiz/easy/result?time=${encodeURIComponent(timeTaken)}&misses=${missedCount}`;
      });
    }
  }