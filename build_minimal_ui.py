import os

# --- 1. OVERWRITE HTML FOR MINIMAL LAYOUT ---
html_path = "frontend/index.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Siddique AI</title>
    <link rel="stylesheet" href="css/style.css">
    <!-- Google Fonts for that sleek dev look -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Minimal Top Navbar -->
    <nav class="navbar">
        <div class="logo"><span>>_</span> siddique-ai</div>
        <div class="nav-links">
            <a href="#" id="new-chat-btn">New Chat</a>
            <a href="#" id="history-toggle">History</a>
        </div>
    </nav>

    <!-- Hidden Sidebar for History (toggled via JS) -->
    <aside class="sidebar" id="sidebar">
        <div class="history-list" id="history-list"></div>
    </aside>

    <main class="main-content">
        <!-- Center Hero (Disappears when chatting) -->
        <div class="hero-section" id="hero-section">
            <h1>Understand what your code<br>is really doing.</h1>
            <p>Analyze architecture, debug hardware, and generate components — all in one place.</p>
        </div>

        <!-- Chat Area -->
        <div class="chat-container" id="chat-container"></div>

        <!-- Floating Input Area -->
        <div class="input-wrapper">
            <div class="input-box">
                <span class="attachment-icon" id="attach-btn" title="Attach Image">📎</span>
                <textarea id="message-input" placeholder="Message Siddique AI..." rows="1"></textarea>
                <button id="send-btn">Analyze ➔</button>
            </div>
            <div class="input-footer">
                <span class="status-dot"></span> API online – v1.0.0
            </div>
        </div>
    </main>

    <input type="file" id="file-input" style="display: none;" accept="image/*">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="js/app.js"></script>
</body>
</html>
""")

# --- 2. OVERWRITE CSS FOR THE NEW VIBE ---
css_path = "frontend/css/style.css"
with open(css_path, "w", encoding="utf-8") as f:
    f.write("""
/* --- Minimal Dark Theme --- */
:root {
    --bg-deep: #09090b;       /* Nearly black */
    --bg-surface: #18181b;    /* Slightly lighter for elements */
    --border-color: #27272a;  /* Subtle borders */
    --text-main: #fafafa;     /* Crisp white text */
    --text-muted: #a1a1aa;    /* Grey text */
    --maroon-primary: #9f1239; /* Modern sleek maroon */
    --maroon-hover: #be123c;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-deep);
    color: var(--text-main);
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
}

/* Navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 40px;
    border-bottom: 1px solid var(--border-color);
}
.logo {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 16px;
    letter-spacing: -0.5px;
}
.logo span {
    color: var(--maroon-primary);
}
.nav-links a {
    color: var(--text-muted);
    text-decoration: none;
    margin-left: 20px;
    font-size: 14px;
    transition: color 0.2s;
}
.nav-links a:hover {
    color: var(--text-main);
}

/* Sidebar Overlay */
.sidebar {
    position: absolute;
    top: 61px;
    right: -300px;
    width: 300px;
    height: calc(100vh - 61px);
    background: var(--bg-surface);
    border-left: 1px solid var(--border-color);
    padding: 20px;
    transition: right 0.3s ease;
    z-index: 100;
}
.sidebar.active {
    right: 0;
}

/* Main Content Area */
.main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    width: 100%;
    max-width: 900px;
    margin: 0 auto;
}

/* Hero Section */
.hero-section {
    position: absolute;
    top: 40%;
    transform: translateY(-50%);
    text-align: left;
    width: 100%;
    padding: 0 40px;
    transition: opacity 0.3s ease;
}
.hero-section h1 {
    font-family: 'JetBrains Mono', monospace;
    font-size: 42px;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 16px;
}
.hero-section p {
    color: var(--text-muted);
    font-size: 16px;
    max-width: 600px;
}

/* Chat Container */
.chat-container {
    flex: 1;
    width: 100%;
    padding: 40px 40px 120px 40px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 24px;
    z-index: 10;
}

/* Individual Messages */
.message {
    max-width: 85%;
    line-height: 1.6;
}
.user-msg {
    align-self: flex-end;
    background: var(--bg-surface);
    padding: 12px 18px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
}
.ai-msg {
    align-self: flex-start;
}

/* Input Area */
.input-wrapper {
    position: absolute;
    bottom: 40px;
    width: 100%;
    max-width: 700px;
    padding: 0 20px;
    z-index: 20;
}
.input-box {
    display: flex;
    align-items: center;
    background: transparent;
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 8px 12px;
    background: var(--bg-deep);
    transition: border-color 0.2s;
}
.input-box:focus-within {
    border-color: var(--maroon-primary);
}
.attachment-icon {
    cursor: pointer;
    padding: 8px;
    font-size: 18px;
    color: var(--text-muted);
    transition: color 0.2s;
}
.attachment-icon:hover {
    color: var(--text-main);
}
textarea {
    flex: 1;
    background: transparent;
    border: none;
    color: var(--text-main);
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    padding: 8px 12px;
    resize: none;
    outline: none;
}
textarea::placeholder {
    color: var(--text-muted);
}
#send-btn {
    background: var(--bg-surface);
    color: var(--text-main);
    border: 1px solid var(--border-color);
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s;
}
#send-btn:hover {
    background: var(--maroon-primary);
    border-color: var(--maroon-primary);
}

.input-footer {
    margin-top: 12px;
    font-size: 12px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 8px;
}
.status-dot {
    width: 8px;
    height: 8px;
    background-color: #22c55e;
    border-radius: 50%;
}
""")

# --- 3. PATCH JS TO HIDE HERO & TOGGLE SIDEBAR ---
js_path = "frontend/js/app.js"
with open(js_path, "r", encoding="utf-8") as f:
    js_code = f.read()

# Add logic to hide the hero section when the first message is sent/loaded
if "document.getElementById('hero-section').style.display = 'none';" not in js_code:
    # Inject it right into the sendMessage function
    js_code = js_code.replace(
        "async function sendMessage() {",
        "async function sendMessage() {\n    document.getElementById('hero-section').style.display = 'none';"
    )
    # Inject it into loadConversation
    js_code = js_code.replace(
        "async function loadConversation(id) {",
        "async function loadConversation(id) {\n    document.getElementById('hero-section').style.display = 'none';"
    )

# Add event listener for the new History toggle button
history_toggle_logic = """
// Sidebar toggle logic
const historyToggle = document.getElementById('history-toggle');
const sidebar = document.getElementById('sidebar');
if(historyToggle && sidebar) {
    historyToggle.addEventListener('click', (e) => {
        e.preventDefault();
        sidebar.classList.toggle('active');
    });
}
"""
if "historyToggle.addEventListener" not in js_code:
    js_code += "\n" + history_toggle_logic

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_code)

print("✅ UI overhauled to Minimal Terminal style.")