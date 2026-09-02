const API_URL = 'https://siddique-ai.onrender.com';
let currentConversationId = null;
let base64Image = null;
let token = localStorage.getItem('siddique_token');

// DOM Elements
const historyList = document.getElementById('history-list');
const chatContainer = document.getElementById('chat-container');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const newChatBtn = document.getElementById('new-chat-btn');
const attachBtn = document.getElementById('attach-btn');
const fileInput = document.getElementById('file-input');
const heroSection = document.getElementById('hero-section');
const disconnectBtn = document.querySelector('.disconnect-btn');

// Auth Overlay
const loginOverlay = document.getElementById('login-overlay');
const loginBtn = document.getElementById('login-btn');

function checkAuth() {
    if (!token) {
        if (loginOverlay) loginOverlay.style.display = 'flex';
    } else {
        if (loginOverlay) loginOverlay.style.display = 'none';
        loadConversations();
    }
}

if (loginBtn) {
    loginBtn.addEventListener('click', async () => {
        const u = document.getElementById('login-username').value;
        const p = document.getElementById('login-password').value;
        try {
            const res = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({ username: u, password: p })
            });
            if (res.ok) {
                const data = await res.json();
                token = data.access_token;
                localStorage.setItem('siddique_token', token);
                checkAuth();
            } else {
                document.getElementById('login-error').style.display = 'block';
            }
        } catch (e) {
            document.getElementById('login-error').textContent = 'Network error.';
            document.getElementById('login-error').style.display = 'block';
        }
    });
}

// Fetch Interceptor
const originalFetch = window.fetch;
window.fetch = async (...args) => {
    let [resource, config] = args;
    if (!config) config = {};
    if (!config.headers) config.headers = {};
    
    if (token && typeof resource === 'string' && !resource.includes('/auth/login')) {
        config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await originalFetch(resource, config);
    if (response.status === 401) {
        localStorage.removeItem('siddique_token');
        token = null;
        checkAuth();
    }
    return response;
};

// Disconnect Button
if (disconnectBtn) {
    disconnectBtn.addEventListener('click', () => {
        localStorage.removeItem('siddique_token');
        token = null;
        chatContainer.innerHTML = '';
        currentConversationId = null;
        if (heroSection) heroSection.style.display = 'block';
        checkAuth();
    });
}

// UI Helpers
function scrollToBottom() {
    chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
}
function hideHero() {
    if (heroSection) heroSection.style.display = 'none';
}

// API Logic
async function loadConversations() {
    try {
        const res = await fetch(`${API_URL}/conversations`);
        if (!res.ok) return;
        const data = await res.json();
        historyList.innerHTML = '';
        data.forEach(conv => {
            const div = document.createElement('div');
            div.className = 'history-item';
            div.textContent = conv.title || 'New Chat';
            div.onclick = () => loadConversation(conv.id);
            if (conv.id === currentConversationId) div.classList.add('active');
            historyList.appendChild(div);
        });
    } catch (e) {
        console.error("History fetch error:", e);
    }
}

async function loadConversation(id) {
    currentConversationId = parseInt(id);
    hideHero();
    try {
        const res = await fetch(`${API_URL}/conversations/${id}`);
        const data = await res.json();
        chatContainer.innerHTML = '';
        data.messages.forEach(msg => {
            const div = document.createElement('div');
            div.className = `message ${msg.role === 'user' ? 'user-msg' : 'ai-msg'}`;
            div.innerHTML = msg.role === 'user' ? msg.content : marked.parse(msg.content);
            chatContainer.appendChild(div);
        });
        loadConversations();
        scrollToBottom();
    } catch (e) {
        console.error("Failed to load conversation history.");
    }
}

async function sendMessage() {
    const text = messageInput.value.trim();
    if (!text && !base64Image) return;

    hideHero();
    
    const userDiv = document.createElement('div');
    userDiv.className = 'message user-msg';
    userDiv.textContent = text + (base64Image ? " [Image Attached]" : "");
    chatContainer.appendChild(userDiv);
    
    messageInput.value = '';
    messageInput.style.height = 'auto'; 
    let currentImage = base64Image;
    base64Image = null;
    attachBtn.style.color = 'var(--text-muted)';
    scrollToBottom();

    const aiDiv = document.createElement('div');
    aiDiv.className = 'message ai-msg';
    chatContainer.appendChild(aiDiv);

    // FIX FOR 422 ERROR: Only add keys if they have valid data, NEVER send null!
    const requestPayload = {
        message: text
    };
    if (currentConversationId) {
        requestPayload.conversation_id = parseInt(currentConversationId);
    }
    if (currentImage) {
        requestPayload.image_base64 = currentImage;
    }

    try {
        const res = await fetch(`${API_URL}/chat/stream`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestPayload)
        });

        if (!res.ok) throw new Error("Network response was not ok");

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let fullText = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk.split('\n\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const dataStr = line.replace('data: ', '');
                    if (dataStr.trim() === '[DONE]') {
                        loadConversations();
                        break;
                    }
                    try {
                        const parsed = JSON.parse(dataStr);
                        if (parsed.content) {
                            fullText += parsed.content;
                            aiDiv.innerHTML = marked.parse(fullText);
                            scrollToBottom();
                        }
                        if (parsed.conversation_id) {
                            currentConversationId = parseInt(parsed.conversation_id);
                        }
                    } catch (e) {}
                }
            }
        }
    } catch (e) {
        aiDiv.innerHTML = "<em>Error connecting to API.</em>";
    }
}

// Event Listeners
if(sendBtn) sendBtn.addEventListener('click', sendMessage);

if(messageInput) {
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
}

if(newChatBtn) {
    newChatBtn.addEventListener('click', () => {
        currentConversationId = null;
        chatContainer.innerHTML = '';
        if (heroSection) heroSection.style.display = 'block';
        loadConversations();
    });
}

if(attachBtn) {
    attachBtn.addEventListener('click', () => fileInput.click());
}
if(fileInput) {
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (evt) => {
                base64Image = evt.target.result.split(',')[1];
                attachBtn.style.color = 'var(--maroon-primary)';
            };
            reader.readAsDataURL(file);
        }
    });
}

// Boot up
checkAuth();
