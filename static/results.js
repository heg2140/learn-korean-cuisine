document.addEventListener("DOMContentLoaded", () => {
    console.log("📣 easy_results.js is loaded"); // test to confirm script is working
  
    // Get values from localStorage
    const time = localStorage.getItem("easyQuizTime");
    const missed = localStorage.getItem("easyQuizMissed");
  
    // Display the values if they exist
    if (time) {
      const timeSpan = document.getElementById("result-time");
      if (timeSpan) timeSpan.textContent = time;
    }
  
    if (missed !== null) {
      const missedSpan = document.getElementById("result-missed");
      if (missedSpan) missedSpan.textContent = missed;
    }
  
    // Optional: clear the data so it doesn’t persist
    localStorage.removeItem("easyQuizTime");
    localStorage.removeItem("easyQuizMissed");
  });
  