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
        const resultBox = document.getElementById("result");
        if (resultBox) {
          resultBox.innerText = `❌ ${ingredient} does not belong in ${targetDish}. Try again!`;
        }
      }
    });
  });
  
  function toggleStar(button) {
    button.classList.toggle("favorited");
  }

  window.addEventListener('load', () => {
    const popup = document.getElementById('flipPopup');
    popup.classList.add('show');
    setTimeout(() => {
      popup.classList.remove('show');
    }, 3000); // hides after 3 seconds
  });