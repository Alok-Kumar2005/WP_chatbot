document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chatBox');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
  
    // Helper: Append new message to chat
    function appendMessage(text, sender) {
      const msgDiv = document.createElement('div');
      msgDiv.classList.add('message', sender);
      msgDiv.textContent = text;
      chatBox.appendChild(msgDiv);
      chatBox.scrollTop = chatBox.scrollHeight; 
    }
  
    // Send user input to backend, then display AI response
    function sendMessage() {
      const text = userInput.value.trim();
      if (!text) return;
      appendMessage(text, 'user');   
      userInput.value = '';        
  
      fetch('/get_response', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          appendMessage(data.message, 'ai'); // AI code output
        } else {
          appendMessage('Error: ' + data.message, 'ai');
        }
      })
      .catch(err => {
        appendMessage('Error: ' + err, 'ai');
      });
    }
  
    // Event listeners
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        sendMessage();
      }
    });
  });
  