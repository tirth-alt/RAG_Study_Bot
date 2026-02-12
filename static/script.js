const API_URL = 'http://localhost:8000';

let isLoading = false;
let sessionId = null;  // Track session ID

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkAPIHealth();
    autoResizeTextarea();
});

// Auto-resize textarea
function autoResizeTextarea() {
    const textarea = document.getElementById('messageInput');
    textarea.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });

    // Submit on Enter (but allow Shift+Enter for new line)
    textarea.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            document.querySelector('.input-form').dispatchEvent(new Event('submit'));
        }
    });
}

// Check API health
async function checkAPIHealth() {
    const statusEl = document.getElementById('status');
    try {
        const response = await fetch(`${API_URL}/api/health`);
        if (response.ok) {
            statusEl.textContent = '✓ Connected to tutor';
            statusEl.className = 'status connected';
        } else {
            throw new Error('API not responding');
        }
    } catch (error) {
        statusEl.textContent = '⚠ API not connected. Make sure API is running.';
        statusEl.className = 'status error';
    }
}

// Send message
async function sendMessage(event) {
    event.preventDefault();

    if (isLoading) return;

    const input = document.getElementById('messageInput');
    const question = input.value.trim();

    if (!question) return;

    // Clear input
    input.value = '';
    input.style.height = 'auto';

    // Hide welcome message
    const welcomeMsg = document.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    // Add user message
    addMessage(question, 'user');

    // Add loading indicator
    const loadingId = addLoading();

    // Disable input
    isLoading = true;
    document.getElementById('sendBtn').disabled = true;

    try {
        const response = await fetch(`${API_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question,
                session_id: sessionId  // Send session ID
            })
        });

        if (!response.ok) {
            throw new Error('Failed to get response');
        }

        const data = await response.json();

        // Store session ID from response
        if (data.session_id) {
            sessionId = data.session_id;
        }

        // Remove loading
        removeLoading(loadingId);

        // Add assistant message
        addMessage(data.answer, 'assistant', data.sources);

    } catch (error) {
        removeLoading(loadingId);
        addMessage('Sorry, I encountered an error. Please make sure the API is running.', 'assistant');
        console.error('Error:', error);
    } finally {
        isLoading = false;
        document.getElementById('sendBtn').disabled = false;
        input.focus();
    }
}

// Add message to chat
function addMessage(text, role, sources = null) {
    const chatContainer = document.getElementById('chatContainer');

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    let messageHTML = `
        <div class="message-content">
            <div class="message-text">${formatText(text)}</div>
    `;

    if (sources && sources.length > 0) {
        messageHTML += `
            <div class="sources">
                <div class="sources-title">📚 Sources</div>
                ${sources.map(source => `
                    <div class="source-item">
                        <span class="source-badge">${source.subject}</span>
                        <span>${source.filename} - Page ${source.page}</span>
                    </div>
                `).join('')}
            </div>
        `;
    }

    messageHTML += `</div>`;
    messageDiv.innerHTML = messageHTML;

    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Format text (preserve line breaks and add basic formatting)
function formatText(text) {
    return text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/• /g, '• ');
}

// Add loading indicator
function addLoading() {
    const chatContainer = document.getElementById('chatContainer');
    const loadingDiv = document.createElement('div');
    const loadingId = 'loading-' + Date.now();
    loadingDiv.id = loadingId;
    loadingDiv.className = 'message assistant';
    loadingDiv.innerHTML = `
        <div class="message-content">
            <div class="loading">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>
        </div>
    `;
    chatContainer.appendChild(loadingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return loadingId;
}

// Remove loading indicator
function removeLoading(loadingId) {
    const loadingEl = document.getElementById(loadingId);
    if (loadingEl) {
        loadingEl.remove();
    }
}

// Clear chat
async function clearChat() {
    if (!confirm('Clear chat history?')) return;

    try {
        await fetch(`${API_URL}/api/clear${sessionId ? '?session_id=' + sessionId : ''}`, { method: 'POST' });
        sessionId = null;  // Reset session

        const chatContainer = document.getElementById('chatContainer');
        chatContainer.innerHTML = `
            <div class="welcome-message">
                <h2>Welcome! 👋</h2>
                <p>I'm your AI tutor for CBSE Class 10 Social Science.</p>
                <div class="suggestions">
                    <p class="suggestions-title">Try asking:</p>
                    <button class="suggestion-chip" onclick="askQuestion('What is democracy?')">
                        What is democracy?
                    </button>
                    <button class="suggestion-chip" onclick="askQuestion('Explain nationalism in brief')">
                        Explain nationalism in brief
                    </button>
                    <button class="suggestion-chip" onclick="askQuestion('What are the features of federalism?')">
                        What are the features of federalism?
                    </button>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error clearing chat:', error);
    }
}

// Ask a suggested question
function askQuestion(question) {
    const input = document.getElementById('messageInput');
    input.value = question;
    input.focus();
    document.querySelector('.input-form').dispatchEvent(new Event('submit'));
}
