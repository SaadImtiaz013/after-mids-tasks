const chatWindow = document.getElementById('chat-window');
const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message-input');
const typingIndicator = document.getElementById('typing-indicator');
const personaSelector = document.getElementById('persona-selector');

// Clear chat when changing persona (Optional visual cue)
personaSelector.addEventListener('change', () => {
    chatWindow.innerHTML = '';
    appendMessage('bot', `<i>System: Switched to ${personaSelector.options[personaSelector.selectedIndex].text}. Memory cleared.</i>`, true);
});

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = messageInput.value.trim();
    // Get the currently selected persona
    const selectedPersona = personaSelector.value;

    if (!message) return;

    appendMessage('user', message);
    messageInput.value = '';

    typingIndicator.classList.remove('hidden');
    scrollToBottom();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message: message, 
                persona: selectedPersona // SEND PERSONA HERE
            })
        });
        const data = await response.json();

        typingIndicator.classList.add('hidden');
        
        if (data.reply) {
            const rawHtml = marked.parse(data.reply);
            appendMessage('bot', rawHtml, true);
        } else {
            appendMessage('bot', "⚠️ Error: Could not get response.");
        }

    } catch (error) {
        typingIndicator.classList.add('hidden');
        console.error(error);
    }
});
function appendMessage(sender, text, isHtml = false) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    const bubble = document.createElement('div');
    bubble.classList.add('bubble');
    if (isHtml) {
        bubble.innerHTML = text;
    } else {
        bubble.textContent = text;
    }
    msgDiv.appendChild(bubble);
    chatWindow.appendChild(msgDiv);
    scrollToBottom();
}
function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
}