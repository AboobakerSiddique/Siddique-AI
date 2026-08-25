
const API_URL = 'http://127.0.0.1:8000';
let token = localStorage.getItem('siddque_token');
let currentConversationId = null;

// DOM Elements
const authScreen = document.getElementById('auth-screen');
const chatScreen = document.getElementById('chat-screen');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');
const authError = document.getElementById('auth-error');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const messagesContainer = document.getElementById('messages-container');
const emptyState = document.querySelector('.empty-state');
const conversationList = document.querySelector('.conversation-list');
const newChatBtn = document.querySelector('.new-chat-btn');

// Initialization
if (token) {
    showChat();
}

// Authentication
loginBtn.addEventListener('click', async () => {
    const username = emailInput.value;
    const password = passwordInput.value;
    authError.textContent = '';

    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const res = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });

        if (!res.ok) throw new Error('Invalid credentials');
        
        const data = await res.json();
        token = data.access_token;
        localStorage.setItem('siddque_token', token);
        showChat();
    } catch (err) {
        authError.textContent = err.message;
    }
});

logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('siddque_token');
    token = null;
    currentConversationId = null;
    chatScreen.classList.add('hidden');
    authScreen.classList.remove('hidden');
    emailInput.value = '';
    passwordInput.value = '';
});

function showChat() {
    authScreen.classList.add('hidden');
    chatScreen.classList.remove('hidden');
    loadConversations();
    chatInput.focus();
}

// --- CONVERSATION LOGIC ---

async function loadConversations() {
    try {
        const res = await fetch(`${API_URL}/conversations`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.status === 401) return logoutBtn.click();
        const convos = await res.json();
        
        conversationList.innerHTML = '';
        convos.forEach(c => {
            const div = document.createElement('div');
            div.className = `conv-item ${c.id === currentConversationId ? 'active' : ''}`;
            div.textContent = c.title;
            div.onclick = () => loadConversation(c.id);
            conversationList.appendChild(div);
        });
    } catch(e) { console.error('Error loading conversations:', e); }
}

async function loadConversation(id) {
    currentConversationId = id;
    try {
        const res = await fetch(`${API_URL}/conversations/${id}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.status === 401) return logoutBtn.click();
        const conv = await res.json();
        
        // Clear screen and hide empty state
        Array.from(messagesContainer.children).forEach(child => {
            if (child !== emptyState) child.remove();
        });
        emptyState.style.display = 'none';
        
        conv.messages.forEach(m => appendMessage(m.role, m.content));
        loadConversations(); // Re-render to update the active highlight
        scrollToBottom();
    } catch(e) { console.error('Error loading conversation:', e); }
}

newChatBtn.addEventListener('click', () => {
    currentConversationId = null;
    Array.from(messagesContainer.children).forEach(child => {
        if (child !== emptyState) child.remove();
    });
    emptyState.style.display = 'block';
    loadConversations(); // Removes active highlight
    chatInput.focus();
});

// --- MESSAGING LOGIC ---

chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);

async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;
    
    emptyState.style.display = 'none';

    appendMessage('user', text);
    chatInput.value = '';
    
    const assistantDiv = document.createElement('div');
    assistantDiv.className = 'message assistant';
    messagesContainer.appendChild(assistantDiv);
    scrollToBottom();

    const payload = { message: text };
    if (currentConversationId) {
        payload.conversation_id = currentConversationId;
    }

    try {
        const res = await fetch(`${API_URL}/chat/stream`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        if (res.status === 401) return logoutBtn.click();

        const reader = res.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let fullResponse = '';
        let isFirstMessage = (currentConversationId === null);

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk.split('\n');
            
            for (let line of lines) {
                if (line.startsWith('data: ')) {
                    const dataStr = line.substring(6);
                    if (dataStr.trim() === '[DONE]') break;
                    
                    try {
                        const parsed = JSON.parse(dataStr);
                        // Backend sends conversation_id at the start of the stream
                        if (parsed.conversation_id) {
                            currentConversationId = parsed.conversation_id;
                            if (isFirstMessage) loadConversations(); // Refresh sidebar to show new title
                        }
                        
                        if (parsed.text) {
                            fullResponse += parsed.text;
                            assistantDiv.innerHTML = marked.parse(fullResponse);
                            scrollToBottom();
                        }
                    } catch (e) { }
                }
            }
        }
    } catch (err) {
        assistantDiv.innerHTML = `<span style="color: #ff5555;">Error connecting to Siddique AI.</span>`;
    }
}

function appendMessage(role, content) {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    div.innerHTML = role === 'user' ? content.replace(/\n/g, '<br>') : marked.parse(content);
    messagesContainer.appendChild(div);
}

function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
