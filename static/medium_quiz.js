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
    
        if (!draggedItem) return;
        if (zone.children.length > 1) return; // prevent multiple drops
    
        const wasCorrect = draggedItem.id === correctAnswer;
    
        // ✅ Log the attempt
        fetch("/quiz/medium/log-answer", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            match_id: draggedItem.id,
            source_type: "label",  // or "ingredient" if you track that
            target_type: "dropzone",
            is_correct: wasCorrect
          })
        });
    
        if (wasCorrect) {
            // Correct match
            zone.appendChild(draggedItem);
            correctCount++;
    
            draggedItem.setAttribute("draggable", "false");
            draggedItem.style.cursor = "default";
    
            zone.classList.add("matched");
            draggedItem.classList.add("matched");
        } else {
            // Incorrect match
            missedCount++;
    
            zone.classList.add("incorrect");
            draggedItem.classList.add("incorrect");
    
            // Return item to original container
            const originalContainer = document.getElementById(`container-${draggedItem.id}`);
            originalContainer.appendChild(draggedItem);
    
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
    clearInterval(timerInterval);
  
    // Get actual remaining time
    const timeText = document.getElementById("timer").textContent;
    const [minStr, secStr] = timeText.split(":");
    const timeLeft = parseInt(minStr) * 60 + parseInt(secStr);
    const timeTaken = 60 - timeLeft;
  
    // Store result before redirect
    fetch("/quiz/medium/store-result", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        outcome: "failed",
        time: `${Math.floor(timeTaken / 60)}:${(timeTaken % 60).toString().padStart(2, '0')}`,
        misses: missedCount,
        matches: correctCount
      })
    })
    .catch(err => console.error("Medium quiz logging failed:", err))
    .finally(() => {
      window.location.href = `/quiz/medium/failed?time=${Math.floor(timeTaken / 60)}:${(timeTaken % 60).toString().padStart(2, '0')}&misses=${missedCount}`;
    });
  }
  

function checkCompletion() {
    if (correctCount === totalQuestions) {
      clearInterval(timerInterval);
      const timeTaken = document.getElementById("timer").textContent;
  
      fetch("/quiz/medium/store-result", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          outcome: "won",
          time: timeTaken,
          misses: missedCount,
          matches: correctCount
        })
      })
      .catch(err => console.error("Medium quiz result logging failed:", err))
      .finally(() => {
        window.location.href = `/quiz/medium/result?time=${encodeURIComponent(timeTaken)}&misses=${missedCount}`;
      });
    }
  }
