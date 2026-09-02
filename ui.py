import os
import re
import time

html_path = "frontend/index.html"
css_path = "frontend/css/style.css"
js_path = "frontend/js/app.js"

cache_buster = str(int(time.time()))

# --- 1. RECOVER API URL ---
api_url = "https://siddique-ai.onrender.com"
if os.path.exists(js_path):
    with open(js_path, "r", encoding="utf-8") as f:
        match = re.search(r"const\s+API_URL\s*=\s*['\"]([^'\"]+)['\"]", f.read())
        if match:
            api_url = match.group(1)

# --- 2. HTML: EXACT PAST UI + LOGIN OVERLAY + CACHE BUSTER ---
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Siddique AI</title>
    <link rel="stylesheet" href="css/style.css?v={cache_buster}">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Login Overlay -->
    <div id="login-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: var(--bg-deep); z-index: 9999; display: flex; flex-direction: column; justify-content: center; align-items: center;">
        <h1 style="font-size: 32px; font-weight: 500; margin-bottom: 20px;">Siddique <span class="accent">AI</span></h1>
        <div style="background: var(--bg-surface); padding: 30px; border-radius: 12px; border: 1px solid var(--border-color); width: 300px; display: flex; flex-direction: column; gap: 15px;">
            <input type="text" id="login-username" placeholder="Username" style="padding: 10px; border-radius: 8px; border: 1px solid var(--border-color); background: var(--bg-deep); color: var(--text-main); outline: none;">
            <input type="password" id="login-password" placeholder="Password" style="padding: 10px; border-radius: 8px; border: 1px solid var(--border-color); background: var(--bg-deep); color: var(--text-main); outline: none;">
            <button id="login-btn" style="padding: 10px; border-radius: 8px; border: none; background: var(--maroon-primary); color: white; font-weight: 500; cursor: pointer;">Login</button>
            <div id="login-error" style="color: #ef4444; font-size: 13px; text-align: center; display: none;">Invalid credentials</div>
        </div>
    </div>

    <div class="app-layout">
        <aside class="sidebar">
            <div class="sidebar-header">
                <span class="logo">Siddique <span class="accent">AI</span></span>
            </div>
            <div class="sidebar-actions">
                <button id="new-chat-btn" class="new-chat-btn">+ New Chat</button>
            </div>
            <div class="history-list" id="history-list"></div>
            <div class="sidebar-footer">
                <button class="disconnect-btn">Disconnect</button>
            </div>
        </aside>

        <main class="main-content">
            <div class="hero-section" id="hero-section">
                <h1>Siddique <span class="accent">AI</span></h1>
                <p>System ready. What are we building?</p>
            </div>

            <div class="chat-container" id="chat-container"></div>

            <div class="input-wrapper">
                <button class="attach-btn" id="attach-btn" title="Attach Image">📎</button>
                <div class="input-box">
                    <textarea id="message-input" placeholder="Message Siddique AI... (Shift+Enter for newline)" rows="1"></textarea>
                    <span class="status-dot-input"></span>
                </div>
                <button class="send-btn" id="send-btn">Send</button>
            </div>
        </main>
    </div>

    <input type="file" id="file-input" style="display: none;" accept="image/*">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="js/app.js?v={cache_buster}"></script>
</body>
</html>
"""

# --- 3. CSS: EXACT PAST UI STYLING ---
css_content = """
:root {
    --bg-deep: #0a0a0a;       
    --bg-sidebar: #111111;    
    --bg-surface: #1a1a1a;    
    --border-color: #2a2a2a;  
    --text-main: #e0e0e0;     
    --text-muted: #888888;    
    --maroon-primary: #9f1239; 
    --maroon-hover: #be123c;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body { font-family: 'Inter', sans-serif; background-color: var(--bg-deep); color: var(--text-main); height: 100vh; overflow: hidden; }
.app-layout { display: flex; height: 100%; }

/* Sidebar */
.sidebar { width: 260px; background-color: var(--bg-sidebar); border-right: 1px solid var(--border-color); display: flex; flex-direction: column; }
.sidebar-header { padding: 20px; }
.logo { font-size: 18px; font-weight: 500; color: var(--text-main); }
.accent { color: var(--maroon-primary); }

.sidebar-actions { padding: 0 20px 20px 20px; }
.new-chat-btn { width: 100%; background: transparent; border: 1px solid var(--border-color); color: var(--text-main); padding: 12px; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 500; transition: border-color 0.2s; }
.new-chat-btn:hover { border-color: var(--maroon-primary); }

.history-list { flex: 1; overflow-y: auto; padding: 0 10px; }
.history-item { padding: 12px 15px; margin-bottom: 4px; border-radius: 6px; cursor: pointer; font-size: 13px; color: var(--text-muted); transition: background 0.2s, color 0.2s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.history-item:hover, .history-item.active { background: var(--bg-surface); color: var(--text-main); }

.sidebar-footer { padding: 20px; }
.disconnect-btn { width: 100%; background: transparent; border: 1px solid var(--border-color); color: var(--text-muted); padding: 10px; border-radius: 8px; cursor: pointer; font-size: 13px; transition: color 0.2s, border-color 0.2s; }
.disconnect-btn:hover { color: var(--text-main); border-color: var(--text-muted); }

/* Main Content */
.main-content { flex: 1; display: flex; flex-direction: column; position: relative; align-items: center; }

.hero-section { position: absolute; top: 40%; transform: translateY(-50%); text-align: center; width: 100%; transition: opacity 0.3s ease; }
.hero-section h1 { font-size: 32px; font-weight: 500; margin-bottom: 15px; letter-spacing: 0.5px; }
.hero-section p { color: var(--text-muted); font-size: 15px; }

.chat-container { flex: 1; width: 100%; max-width: 800px; padding: 40px 20px 140px 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 24px; z-index: 10; }
.message { max-width: 85%; line-height: 1.6; font-size: 15px; }
.user-msg { align-self: flex-end; background: var(--bg-surface); padding: 12px 18px; border-radius: 12px; border: 1px solid var(--border-color); }
.ai-msg { align-self: flex-start; }

/* Input */
.input-wrapper { position: absolute; bottom: 40px; width: 100%; max-width: 800px; padding: 0 20px; z-index: 20; display: flex; align-items: flex-end; gap: 15px; }
.attach-btn { background: var(--bg-surface); border: 1px solid var(--border-color); color: var(--text-muted); width: 45px; height: 45px; border-radius: 50%; cursor: pointer; font-size: 16px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-bottom: 2px; transition: color 0.2s, border-color 0.2s; }
.attach-btn:hover { color: var(--text-main); border-color: var(--text-muted); }

.input-box { flex: 1; display: flex; align-items: center; background: var(--bg-deep); border: 1px solid var(--maroon-primary); border-radius: 25px; padding: 14px 20px; position: relative; box-shadow: 0 0 10px rgba(159, 18, 57, 0.1); }
textarea { flex: 1; background: transparent; border: none; color: var(--text-main); font-family: 'Inter', sans-serif; font-size: 15px; resize: none; outline: none; max-height: 150px; padding-right: 20px; }
textarea::placeholder { color: var(--text-muted); }

.status-dot-input { width: 6px; height: 6px; background-color: #6d28d9; border-radius: 50%; position: absolute; right: 20px; bottom: 22px; }

.send-btn { background: var(--maroon-primary); color: #fff; border: none; padding: 0 25px; height: 45px; border-radius: 25px; cursor: pointer; font-size: 15px; font-weight: 500; flex-shrink: 0; margin-bottom: 2px; transition: background 0.2s; }
.send-btn:hover { background: var(--maroon-hover); }

/* Markdown Overrides */
.ai-msg pre { background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 8px; padding: 16px; margin: 12px 0; overflow-x: auto; }
"""

# --- 4. JS: FIX 422 PAYLOAD + WIRE DISCONNECT ---
js_content = f"""const API_URL = '{api_url}';
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

function checkAuth() {{
    if (!token) {{
        if (loginOverlay) loginOverlay.style.display = 'flex';
    }} else {{
        if (loginOverlay) loginOverlay.style.display = 'none';
        loadConversations();
    }}
}}

if (loginBtn) {{
    loginBtn.addEventListener('click', async () => {{
        const u = document.getElementById('login-username').value;
        const p = document.getElementById('login-password').value;
        try {{
            const res = await fetch(`${{API_URL}}/auth/login`, {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/x-www-form-urlencoded' }},
                body: new URLSearchParams({{ username: u, password: p }})
            }});
            if (res.ok) {{
                const data = await res.json();
                token = data.access_token;
                localStorage.setItem('siddique_token', token);
                checkAuth();
            }} else {{
                document.getElementById('login-error').style.display = 'block';
            }}
        }} catch (e) {{
            document.getElementById('login-error').textContent = 'Network error.';
            document.getElementById('login-error').style.display = 'block';
        }}
    }});
}}

// Fetch Interceptor
const originalFetch = window.fetch;
window.fetch = async (...args) => {{
    let [resource, config] = args;
    if (!config) config = {{}};
    if (!config.headers) config.headers = {{}};
    
    if (token && typeof resource === 'string' && !resource.includes('/auth/login')) {{
        config.headers['Authorization'] = `Bearer ${{token}}`;
    }}
    
    const response = await originalFetch(resource, config);
    if (response.status === 401) {{
        localStorage.removeItem('siddique_token');
        token = null;
        checkAuth();
    }}
    return response;
}};

// Disconnect Button
if (disconnectBtn) {{
    disconnectBtn.addEventListener('click', () => {{
        localStorage.removeItem('siddique_token');
        token = null;
        chatContainer.innerHTML = '';
        currentConversationId = null;
        if (heroSection) heroSection.style.display = 'block';
        checkAuth();
    }});
}}

// UI Helpers
function scrollToBottom() {{
    chatContainer.scrollTo({{ top: chatContainer.scrollHeight, behavior: 'smooth' }});
}}
function hideHero() {{
    if (heroSection) heroSection.style.display = 'none';
}}

// API Logic
async function loadConversations() {{
    try {{
        const res = await fetch(`${{API_URL}}/conversations`);
        if (!res.ok) return;
        const data = await res.json();
        historyList.innerHTML = '';
        data.forEach(conv => {{
            const div = document.createElement('div');
            div.className = 'history-item';
            div.textContent = conv.title || 'New Chat';
            div.onclick = () => loadConversation(conv.id);
            if (conv.id === currentConversationId) div.classList.add('active');
            historyList.appendChild(div);
        }});
    }} catch (e) {{
        console.error("History fetch error:", e);
    }}
}}

async function loadConversation(id) {{
    currentConversationId = parseInt(id);
    hideHero();
    try {{
        const res = await fetch(`${{API_URL}}/conversations/${{id}}`);
        const data = await res.json();
        chatContainer.innerHTML = '';
        data.messages.forEach(msg => {{
            const div = document.createElement('div');
            div.className = `message ${{msg.role === 'user' ? 'user-msg' : 'ai-msg'}}`;
            div.innerHTML = msg.role === 'user' ? msg.content : marked.parse(msg.content);
            chatContainer.appendChild(div);
        }});
        loadConversations();
        scrollToBottom();
    }} catch (e) {{
        console.error("Failed to load conversation history.");
    }}
}}

async function sendMessage() {{
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
    const requestPayload = {{
        message: text
    }};
    if (currentConversationId) {{
        requestPayload.conversation_id = parseInt(currentConversationId);
    }}
    if (currentImage) {{
        requestPayload.image_base64 = currentImage;
    }}

    try {{
        const res = await fetch(`${{API_URL}}/chat/stream`, {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify(requestPayload)
        }});

        if (!res.ok) throw new Error("Network response was not ok");

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let fullText = "";

        while (true) {{
            const {{ done, value }} = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value, {{ stream: true }});
            const lines = chunk.split('\\n\\n');
            
            for (const line of lines) {{
                if (line.startsWith('data: ')) {{
                    const dataStr = line.replace('data: ', '');
                    if (dataStr.trim() === '[DONE]') {{
                        loadConversations();
                        break;
                    }}
                    try {{
                        const parsed = JSON.parse(dataStr);
                        if (parsed.content) {{
                            fullText += parsed.content;
                            aiDiv.innerHTML = marked.parse(fullText);
                            scrollToBottom();
                        }}
                        if (parsed.conversation_id) {{
                            currentConversationId = parseInt(parsed.conversation_id);
                        }}
                    }} catch (e) {{}}
                }}
            }}
        }}
    }} catch (e) {{
        aiDiv.innerHTML = "<em>Error connecting to API.</em>";
    }}
}}

// Event Listeners
if(sendBtn) sendBtn.addEventListener('click', sendMessage);

if(messageInput) {{
    messageInput.addEventListener('keydown', (e) => {{
        if (e.key === 'Enter' && !e.shiftKey) {{
            e.preventDefault();
            sendMessage();
        }}
    }});

    messageInput.addEventListener('input', function() {{
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    }});
}}

if(newChatBtn) {{
    newChatBtn.addEventListener('click', () => {{
        currentConversationId = null;
        chatContainer.innerHTML = '';
        if (heroSection) heroSection.style.display = 'block';
        loadConversations();
    }});
}}

if(attachBtn) {{
    attachBtn.addEventListener('click', () => fileInput.click());
}}
if(fileInput) {{
    fileInput.addEventListener('change', (e) => {{
        const file = e.target.files[0];
        if (file) {{
            const reader = new FileReader();
            reader.onload = (evt) => {{
                base64Image = evt.target.result.split(',')[1];
                attachBtn.style.color = 'var(--maroon-primary)';
            }};
            reader.readAsDataURL(file);
        }}
    }});
}}

// Boot up
checkAuth();
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
with open(css_path, "w", encoding="utf-8") as f:
    f.write(css_content)
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print("✅ UI matching classic layout generated.")
print("✅ 422 Payload fix applied.")
print("✅ Disconnect wired.")