// script.js

// Select input fields and buttons
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const loginBtn = document.getElementById('login-btn');
const signupBtn = document.getElementById('signup-btn');

// Focus and blur effects for input fields
usernameInput.addEventListener('focus', () => {
  usernameInput.style.borderColor = '#3a7bd5';
});
usernameInput.addEventListener('blur', () => {
  usernameInput.style.borderColor = '#ccc';
});

passwordInput.addEventListener('focus', () => {
  passwordInput.style.borderColor = '#3a7bd5';
});
passwordInput.addEventListener('blur', () => {
  passwordInput.style.borderColor = '#ccc';
});

// Simulate form submission
loginBtn.addEventListener('click', () => {
  alert(`Welcome, ${usernameInput.value}! (Login simulation)`);
});

signupBtn.addEventListener('click', () => {
  alert(`Sign-Up initiated for: ${usernameInput.value}`);
});
