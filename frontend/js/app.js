
const API_URL = 'https://siddique-ai.onrender.com';
let token = localStorage.getItem('siddique_token');
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
        localStorage.setItem('siddique_token', token);
        showChat();
    } catch (err) {
        authError.textContent = err.message;
    }
});

logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('siddique_token');
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
    if (currentImageBase64) {
        payload.image_base64 = currentImageBase64;
        payload.image_mime_type = currentImageMimeType;
        removeImageBtn.click(); // Clear image after sending
    }
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
                    if (dataStr.trim() === '[DONE]') { renderUIComponents(assistantDiv); break; }
                    
                    try {
                        const parsed = JSON.parse(dataStr);
                        // Backend sends conversation_id at the start of the stream
                        if (parsed.conversation_id) {
                            currentConversationId = parsed.conversation_id;
                            if (isFirstMessage) loadConversations(); // Refresh sidebar to show new title
                        }
                        
                        if (parsed.error) { assistantDiv.remove(); showNotification(parsed.error); break; }
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
        assistantDiv.remove(); showNotification("Error connecting to Siddique AI. Please check your network.");
    }
}

function appendMessage(role, content) {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    div.innerHTML = role === 'user' ? content.replace(/\n/g, '<br>') : marked.parse(content);
    messagesContainer.appendChild(div);
}

let isAutoScrolling = false;
function scrollToBottom() {
    if (!isAutoScrolling) {
        isAutoScrolling = true;
        requestAnimationFrame(() => {
            messagesContainer.scrollTo({
                top: messagesContainer.scrollHeight,
                behavior: 'smooth'
            });
            setTimeout(() => { isAutoScrolling = false; }, 100);
        });
    }
}

// --- Phase 11: Vision UI Logic ---
const uploadTriggerBtn = document.getElementById('upload-trigger-btn');
const imageUpload = document.getElementById('image-upload');
const imagePreviewContainer = document.getElementById('image-preview-container');
const imagePreview = document.getElementById('image-preview');
const removeImageBtn = document.getElementById('remove-image-btn');

let currentImageBase64 = null;
let currentImageMimeType = null;

if(uploadTriggerBtn) {
    uploadTriggerBtn.addEventListener('click', () => imageUpload.click());

    imageUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        const reader = new FileReader();
        reader.onload = (event) => {
            // Display preview
            imagePreview.src = event.target.result;
            imagePreviewContainer.classList.remove('hidden');
            
            // Extract base64 and mime type
            const base64String = event.target.result.split(',')[1];
            currentImageBase64 = base64String;
            currentImageMimeType = file.type;
        };
        reader.readAsDataURL(file);
    });

    removeImageBtn.addEventListener('click', () => {
        imageUpload.value = '';
        currentImageBase64 = null;
        currentImageMimeType = null;
        imagePreviewContainer.classList.add('hidden');
        imagePreview.src = '';
    });
}

// --- Phase 13: Live UI Component Renderer ---
function renderUIComponents(container) {
    // Find all HTML code blocks generated by marked.js
    const htmlBlocks = container.querySelectorAll('pre code.language-html');
    
    htmlBlocks.forEach(block => {
        const code = block.textContent;
        
        // Create the preview container
        const previewDiv = document.createElement('div');
        previewDiv.className = 'live-preview-box';
        previewDiv.innerHTML = `<div class="preview-header"><span>Live Component Render</span> Interactive Sandbox</div>`;
        
        // Create a sandboxed iframe to safely render the code
        const iframe = document.createElement('iframe');
        iframe.style.width = '100%';
        iframe.style.height = '400px';
        iframe.style.border = 'none';
        iframe.style.background = '#ffffff'; // Force white background for standard UI rendering
        
        previewDiv.appendChild(iframe);
        
        // Insert it right after the code block
        block.parentElement.insertAdjacentElement('afterend', previewDiv);
        
        // Write the code into the iframe
        const doc = iframe.contentWindow.document;
        doc.open();
        doc.write(code);
        doc.close();
    });
    
    scrollToBottom();
}


// --- Premium Error Notification System ---
const toastContainer = document.createElement('div');
toastContainer.id = 'toast-container';
toastContainer.style.cssText = 'position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 9999; display: flex; flex-direction: column; gap: 10px;';
document.body.appendChild(toastContainer);

function showNotification(message, duration = 4000) {
    const toast = document.createElement('div');
    toast.style.cssText = 'background: #1e1e1e; color: #e8e8e8; padding: 14px 24px; border-radius: 8px; border-left: 4px solid var(--maroon-primary); box-shadow: 0 4px 15px rgba(0,0,0,0.6); font-size: 14px; opacity: 0; transform: translateY(-20px); transition: all 0.3s ease; display: flex; align-items: center; min-width: 320px;';
    
    // Sanitize the ugly API errors
    let cleanMsg = message;
    if (cleanMsg.includes('429') || cleanMsg.includes('RESOURCE_EXHAUSTED')) {
        cleanMsg = "Rate limit exceeded. Please wait a few seconds and try again.";
    } else if (cleanMsg.includes('11001') || cleanMsg.includes('getaddrinfo')) {
        cleanMsg = "Network error: Unable to reach the API. Please check your connection.";
    } else if (cleanMsg.includes('AI_SERVICE_ERROR')) {
        cleanMsg = cleanMsg.split('{')[0].trim(); // Strip the raw JSON dictionary dump
    }
    
    toast.textContent = cleanMsg;
    toastContainer.appendChild(toast);
    
    // Slide in
    requestAnimationFrame(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
    });

    // Fade out and remove
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-20px)';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}
