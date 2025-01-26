// script.js

document.getElementById('file-upload').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
      alert(`You uploaded: ${file.name}`);
    } else {
      alert("No file selected");
    }
  });
  