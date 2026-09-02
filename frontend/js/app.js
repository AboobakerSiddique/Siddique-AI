const API_URL = 'https://siddique-ai.onrender.com';
let currentConversationId = null;
let base64Image = null;

// --- DOM Elements ---
const historyList = document.getElementById('history-list');
const chatContainer = document.getElementById('chat-container');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const newChatBtn = document.getElementById('new-chat-btn');
const attachBtn = document.getElementById('attach-btn');
const fileInput = document.getElementById('file-input');
const heroSection = document.getElementById('hero-section');

// --- UI Helpers ---
function scrollToBottom() {
    chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
}

function hideHero() {
    if (heroSection) heroSection.style.display = 'none';
}

// --- Premium Toast Notifications ---
const toastContainer = document.createElement('div');
toastContainer.id = 'toast-container';
toastContainer.style.cssText = 'position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 9999; display: flex; flex-direction: column; gap: 10px;';
document.body.appendChild(toastContainer);

function showNotification(message, duration = 4000) {
    const toast = document.createElement('div');
    toast.style.cssText = 'background: #1e1e1e; color: #e8e8e8; padding: 14px 24px; border-radius: 8px; border-left: 4px solid var(--maroon-primary); box-shadow: 0 4px 15px rgba(0,0,0,0.6); font-size: 14px; opacity: 0; transform: translateY(-20px); transition: all 0.3s ease; display: flex; align-items: center; min-width: 320px;';
    
    let cleanMsg = message;
    if (cleanMsg.includes('429') || cleanMsg.includes('RESOURCE_EXHAUSTED')) cleanMsg = "Rate limit exceeded. Please wait a few seconds.";
    else if (cleanMsg.includes('11001') || cleanMsg.includes('getaddrinfo')) cleanMsg = "Network error: Unable to reach the API.";
    else if (cleanMsg.includes('AI_SERVICE_ERROR')) cleanMsg = cleanMsg.split('{')[0].trim();
    
    toast.textContent = cleanMsg;
    toastContainer.appendChild(toast);
    
    requestAnimationFrame(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
    });

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-20px)';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// --- Live UI Renderer ---
function renderUIComponents(container) {
    const htmlBlocks = container.querySelectorAll('pre code.language-html');
    htmlBlocks.forEach(block => {
        const code = block.textContent;
        const previewDiv = document.createElement('div');
        previewDiv.className = 'live-preview-box';
        previewDiv.style.cssText = 'margin: 15px 0; border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; background: var(--bg-deep);';
        previewDiv.innerHTML = `<div class="preview-header" style="background: #0c0c0c; padding: 8px 15px; font-size: 12px; color: var(--text-muted); border-bottom: 1px solid var(--border-color);"><span>Live Component Render</span></div>`;
        
        const iframe = document.createElement('iframe');
        iframe.style.width = '100%';
        iframe.style.height = '400px';
        iframe.style.border = 'none';
        iframe.style.background = '#ffffff';
        
        previewDiv.appendChild(iframe);
        block.parentElement.insertAdjacentElement('afterend', previewDiv);
        
        const doc = iframe.contentWindow.document;
        doc.open();
        doc.write(code);
        doc.close();
    });
}

// --- Core API Logic ---
async function loadConversations() {
    try {
        const res = await fetch(`${API_URL}/conversations`);
        if (!res.ok) throw new Error("API not ready");
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
        console.error("History fetch error (Backend might be asleep):", e);
    }
}

async function loadConversation(id) {
    currentConversationId = id;
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
            if(msg.role === 'assistant') renderUIComponents(div);
        });
        
        scrollToBottom();
    } catch (e) {
        showNotification("Failed to load conversation history.");
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

    try {
        const res = await fetch(`${API_URL}/chat/stream`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...(currentConversationId !== null && { conversation_id: currentConversationId }),
                message: text,
                ...(currentImage && { image_base64: currentImage })
            })
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
                        renderUIComponents(aiDiv);
                        
                        break;
                    }
                    try {
                        const parsed = JSON.parse(dataStr);
                        if (parsed.error) {
                            aiDiv.remove();
                            showNotification(parsed.error);
                            break;
                        }
                        if (parsed.content) {
                            fullText += parsed.content;
                            aiDiv.innerHTML = marked.parse(fullText);
                            scrollToBottom();
                        }
                        if (parsed.conversation_id) {
                            currentConversationId = parsed.conversation_id;
                        }
                    } catch (e) {}
                }
            }
        }
    } catch (e) {
        aiDiv.remove();
        showNotification("Error connecting to backend. If on Render, wait 30 seconds for it to wake up.");
    }
}

// --- Event Listeners ---
sendBtn.addEventListener('click', sendMessage);

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

newChatBtn.addEventListener('click', () => {
    currentConversationId = null;
    chatContainer.innerHTML = '';
    if (heroSection) heroSection.style.display = 'block';
    
});

attachBtn.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (evt) => {
            base64Image = evt.target.result.split(',')[1];
            attachBtn.style.color = 'var(--maroon-primary)';
            showNotification("Image attached successfully.", 2000);
        };
        reader.readAsDataURL(file);
    }
});

// Initialize


// --- Authentication ---
const loginOverlay = document.getElementById('login-overlay');
const loginBtn = document.getElementById('login-btn');
let token = localStorage.getItem('siddique_token');

function checkAuth() {
    if (!token) {
        loginOverlay.style.display = 'flex';
    } else {
        loginOverlay.style.display = 'none';
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

// Modify fetch calls to include the token
const originalFetch = window.fetch;
window.fetch = async (...args) => {
    let [resource, config] = args;
    if (!config) config = {};
    if (!config.headers) config.headers = {};
    
    // Don't add token to the login route itself
    if (token && !resource.includes('/auth/login')) {
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

// Replace the old initialize call at the bottom

checkAuth();
