document.querySelectorAll('.draggable').forEach(el => {
    el.addEventListener('dragstart', e => {
      e.dataTransfer.setData("text/plain", e.target.dataset.dish + "|" + e.target.innerText);
    });
  });
  
  document.querySelectorAll('.dropzone').forEach(zone => {
    zone.addEventListener('dragover', e => e.preventDefault());
  
    zone.addEventListener('drop', e => {
      e.preventDefault();
      const [correctDish, ingredient] = e.dataTransfer.getData("text/plain").split("|");
      const targetDish = zone.dataset.dish;
  
      if (correctDish === targetDish) {
        zone.innerHTML += `<div class='correct'>✅ ${ingredient}</div>`;
      } else {
        document.getElementById("result").innerText = `❌ ${ingredient} does not belong in ${targetDish}. Try again!`;
      }
    });
  });
  