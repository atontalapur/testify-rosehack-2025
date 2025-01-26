// script.js

// Chat Functionality
const chatBox = document.getElementById("chat-box");
const chatInput = document.getElementById("chat-input");
const chatSend = document.getElementById("chat-send");

chatSend.addEventListener("click", () => {
  const userMessage = chatInput.value;
  if (userMessage.trim()) {
    const message = document.createElement("p");
    message.textContent = `User: ${userMessage}`;
    chatBox.appendChild(message);

    // Simulate AI response
    const response = document.createElement("p");
    response.textContent = "Testify: This feature is not fully implemented yet.";
    response.style.color = "blue";
    chatBox.appendChild(response);

    chatInput.value = "";
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
  }
});
