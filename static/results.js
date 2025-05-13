document.addEventListener("DOMContentLoaded", () => {
    console.log("📣 easy_results.js is loaded"); 
  
    const time = localStorage.getItem("easyQuizTime");
    const missed = localStorage.getItem("easyQuizMissed");
  
    if (time) {
      const timeSpan = document.getElementById("result-time");
      if (timeSpan) timeSpan.textContent = time;
    }
  
    if (missed !== null) {
      const missedSpan = document.getElementById("result-missed");
      if (missedSpan) missedSpan.textContent = missed;
    }
  
    localStorage.removeItem("easyQuizTime");
    localStorage.removeItem("easyQuizMissed");
  });
  