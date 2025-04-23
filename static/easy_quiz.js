let correctCount = 0;
let missedCount = 0;
let draggedItem = null;
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
    
        checkCompletion(); // call after each drop
    });
    
});

// Timer logic
let startTime = Date.now();
setInterval(() => {
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    const minutes = Math.floor(elapsed / 60);
    const seconds = elapsed % 60;
    document.getElementById("timer").textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
}, 1000);


function checkCompletion() {
    if (correctCount === 3) {
      // ✅ ADD THIS HERE to save data
      const time = document.getElementById("timer").textContent;
      localStorage.setItem("easyQuizTime", time);
      localStorage.setItem("easyQuizMissed", missedCount);
      console.log("Saving to localStorage:", time, missedCount);
  
      // Then go to the results page
      setTimeout(() => {
        window.location.href = "/quiz/easy/result";
      }, 500);
    }
  }