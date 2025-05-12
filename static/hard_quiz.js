let correctCount = 0;
let missedCount = 0;
let draggedItem = null;
const totalQuestions = 5;
let timeLeft = 60;
let timerInterval;

window.addEventListener("load", () => {
  const timerElement = document.getElementById("timer");

  // Make all cards draggable
  document.querySelectorAll(".card").forEach(card => {
    card.addEventListener("dragstart", e => {
      draggedItem = card;
    });

    card.addEventListener("dragover", e => {
      e.preventDefault();
    });

    card.addEventListener("drop", e => {
        e.preventDefault();
        if (!draggedItem || draggedItem === card) return;
      
        const sourceMatchId = draggedItem.dataset.matchId;
        const targetMatchId = card.dataset.matchId;
      
        const sourceType = draggedItem.dataset.type;
        const targetType = card.dataset.type;
      
        if (sourceMatchId === targetMatchId) {
          // ✅ Correct match
          draggedItem.setAttribute("draggable", "false");
          card.setAttribute("draggable", "false");
          draggedItem.style.cursor = "default";
          card.style.cursor = "default";
      
          draggedItem.classList.add("matched");
          card.classList.add("matched");
      
          const wrapper = document.createElement("div");
          wrapper.classList.add("match-nested");
          wrapper.appendChild(card.cloneNode(true));
          wrapper.appendChild(draggedItem);
          card.replaceWith(wrapper);
      
          correctCount++;
      
          // ✅ Log correct match
          fetch("/quiz/hard/log-answer", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              match_id: sourceMatchId,
              source_type: sourceType,
              target_type: targetType,
              is_correct: true
            })
          });
        } else {
          // ❌ Incorrect match
          draggedItem.classList.add("incorrect");
          card.classList.add("incorrect");
      
          missedCount++;
      
          // ✅ Log incorrect match
          fetch("/quiz/hard/log-answer", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              match_id: `${sourceMatchId}→${targetMatchId}`, // distinguish mismatch
              source_type: sourceType,
              target_type: targetType,
              is_correct: false
            })
          });
      
          setTimeout(() => {
            draggedItem.classList.remove("incorrect");
            card.classList.remove("incorrect");
          }, 500);
        }
      
        // update score
        document.getElementById("correct").textContent = correctCount;
        document.getElementById("missed").textContent = missedCount;
      
        checkCompletion();
      });
  });

  // Timer setup
  timerInterval = setInterval(updateTimer, 1000);

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
});

// Completion
function checkCompletion() {
    if (correctCount === totalQuestions) {
      clearInterval(timerInterval);
      const timeTaken = document.getElementById("timer").textContent;
  
      // Send result to backend
      fetch("/quiz/hard/store-result", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          outcome: "won",
          time: timeTaken,
          misses: missedCount,
          matches: correctCount
        })
      })
      .catch(err => {
        console.error("Failed to store result:", err);
      })
      .finally(() => {
        // ✅ Always redirect
        window.location.href = `/quiz/hard/result?time=${encodeURIComponent(timeTaken)}&misses=${missedCount}`;
      });
    }
  }

  function endQuiz() {
    const timeTaken = document.getElementById("timer").textContent;
  
    fetch("/quiz/hard/store-result", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        outcome: "failed",
        time: timeTaken,
        misses: missedCount,
        matches: correctCount
      })
    }).then(() => {
      window.location.href = `/quiz/hard/failed?time=${encodeURIComponent(timeTaken)}&misses=${missedCount}`;
    });
  }

function playCardAudio(button, event) {
  event.stopPropagation();
  const audio = button.closest(".card").querySelector("audio");
  if (audio) audio.play();
}