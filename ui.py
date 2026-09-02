import os

html_path = "frontend/index.html"
js_path = "frontend/js/app.js"
css_path = "frontend/css/style.css"

# --- 1. ADD LOGIN OVERLAY TO HTML ---
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

login_overlay = """
    <div id="login-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: var(--bg-deep); z-index: 9999; display: flex; flex-direction: column; justify-content: center; align-items: center;">
        <h1 style="font-size: 32px; font-weight: 500; margin-bottom: 20px;">Siddique <span class="accent">AI</span></h1>
        <div style="background: var(--bg-surface); padding: 30px; border-radius: 12px; border: 1px solid var(--border-color); width: 300px; display: flex; flex-direction: column; gap: 15px;">
            <input type="text" id="login-username" placeholder="Username" style="padding: 10px; border-radius: 8px; border: 1px solid var(--border-color); background: var(--bg-deep); color: var(--text-main); outline: none;">
            <input type="password" id="login-password" placeholder="Password" style="padding: 10px; border-radius: 8px; border: 1px solid var(--border-color); background: var(--bg-deep); color: var(--text-main); outline: none;">
            <button id="login-btn" style="padding: 10px; border-radius: 8px; border: none; background: var(--maroon-primary); color: white; font-weight: 500; cursor: pointer;">Login</button>
            <div id="login-error" style="color: #ef4444; font-size: 13px; text-align: center; display: none;">Invalid credentials</div>
        </div>
    </div>
"""

if 'id="login-overlay"' not in html:
    html = html.replace("<body>", f"<body>{login_overlay}")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

# --- 2. ADD AUTH LOGIC TO JS ---
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

auth_logic = """
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
"""

if 'localStorage.getItem(\'siddique_token\')' not in js:
    # Remove the old initialization call at the bottom
    js = js.replace("loadConversations();", "")
    # Append the auth logic which handles initialization
    js += auth_logic
    js += "\ncheckAuth();\n"
    
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js)

print("✅ Authentication UI and JWT interception logic restored.")