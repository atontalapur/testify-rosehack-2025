// script.js

const fileInput = document.getElementById("file-upload");
const filePreview = document.getElementById("file-preview");

// Display selected files for preview
fileInput.addEventListener("change", () => {
  const files = fileInput.files;

  if (files.length === 0) {
    filePreview.innerHTML = "<p>No files uploaded yet.</p>";
    return;
  }

  const fileList = document.createElement("ul");
  Array.from(files).forEach((file) => {
    const listItem = document.createElement("li");
    listItem.textContent = `${file.name} (${Math.round(file.size / 1024)} KB)`;
    fileList.appendChild(listItem);
  });

  filePreview.innerHTML = ""; // Clear previous content
  filePreview.appendChild(fileList);
});
