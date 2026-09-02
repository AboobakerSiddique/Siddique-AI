import os

html_path = "frontend/index.html"
css_path = "frontend/css/style.css"

# --- 1. HTML: RESTORE EXACT PAST UI LAYOUT ---
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Siddique AI</title>
    <link rel="stylesheet" href="css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
</head>
<body>
    <div class="app-layout">
        <!-- Sidebar -->
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

        <!-- Main Chat Area -->
        <main class="main-content">
            <!-- Centered Hero -->
            <div class="hero-section" id="hero-section">
                <h1>Siddique <span class="accent">AI</span></h1>
                <p>System ready. What are we building?</p>
            </div>

            <!-- Chat Output -->
            <div class="chat-container" id="chat-container"></div>

            <!-- Input Area matches Past UI image perfectly -->
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
    <script src="js/app.js"></script>
</body>
</html>
"""

# --- 2. CSS: RESTORE PAST UI STYLING ---
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

body {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-deep);
    color: var(--text-main);
    height: 100vh;
    overflow: hidden;
}

.app-layout {
    display: flex;
    height: 100%;
}

/* Sidebar Styling */
.sidebar {
    width: 260px;
    background-color: var(--bg-sidebar);
    border-right: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
}
.sidebar-header {
    padding: 20px;
}
.logo {
    font-size: 18px;
    font-weight: 500;
    color: var(--text-main);
}
.accent {
    color: var(--maroon-primary);
}

.sidebar-actions {
    padding: 0 20px 20px 20px;
}
.new-chat-btn {
    width: 100%;
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-main);
    padding: 12px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: border-color 0.2s;
}
.new-chat-btn:hover {
    border-color: var(--maroon-primary);
}

.history-list {
    flex: 1;
    overflow-y: auto;
    padding: 0 10px;
}
.history-item {
    padding: 12px 15px;
    margin-bottom: 4px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    color: var(--text-muted);
    transition: background 0.2s, color 0.2s;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.history-item:hover, .history-item.active {
    background: var(--bg-surface);
    color: var(--text-main);
}

.sidebar-footer {
    padding: 20px;
}
.disconnect-btn {
    width: 100%;
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-muted);
    padding: 10px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 13px;
    transition: color 0.2s, border-color 0.2s;
}
.disconnect-btn:hover {
    color: var(--text-main);
    border-color: var(--text-muted);
}

/* Main Content Area */
.main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    position: relative;
    align-items: center;
}

/* Hero Section */
.hero-section {
    position: absolute;
    top: 40%;
    transform: translateY(-50%);
    text-align: center;
    width: 100%;
    transition: opacity 0.3s ease;
}
.hero-section h1 {
    font-size: 32px;
    font-weight: 500;
    margin-bottom: 15px;
    letter-spacing: 0.5px;
}
.hero-section p {
    color: var(--text-muted);
    font-size: 15px;
}

/* Chat Output */
.chat-container {
    flex: 1;
    width: 100%;
    max-width: 800px;
    padding: 40px 20px 140px 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 24px;
    z-index: 10;
}
.message {
    max-width: 85%;
    line-height: 1.6;
    font-size: 15px;
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

/* Input Area matches Past UI exactly */
.input-wrapper {
    position: absolute;
    bottom: 40px;
    width: 100%;
    max-width: 800px;
    padding: 0 20px;
    z-index: 20;
    display: flex;
    align-items: flex-end;
    gap: 15px;
}
.attach-btn {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    color: var(--text-muted);
    width: 45px;
    height: 45px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-bottom: 2px;
    transition: color 0.2s, border-color 0.2s;
}
.attach-btn:hover {
    color: var(--text-main);
    border-color: var(--text-muted);
}
.input-box {
    flex: 1;
    display: flex;
    align-items: center;
    background: var(--bg-deep);
    border: 1px solid var(--maroon-primary); /* The distinct red border */
    border-radius: 25px;
    padding: 14px 20px;
    position: relative;
    box-shadow: 0 0 10px rgba(159, 18, 57, 0.1);
}
textarea {
    flex: 1;
    background: transparent;
    border: none;
    color: var(--text-main);
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    resize: none;
    outline: none;
    max-height: 150px;
    padding-right: 20px; /* Space for the status dot */
}
textarea::placeholder { color: var(--text-muted); }

/* The distinct purple dot inside the input */
.status-dot-input {
    width: 6px;
    height: 6px;
    background-color: #6d28d9; 
    border-radius: 50%;
    position: absolute;
    right: 20px;
    bottom: 22px;
}

/* Maroon Send Pill outside the input */
.send-btn {
    background: var(--maroon-primary);
    color: #fff;
    border: none;
    padding: 0 25px;
    height: 45px;
    border-radius: 25px;
    cursor: pointer;
    font-size: 15px;
    font-weight: 500;
    flex-shrink: 0;
    margin-bottom: 2px;
    transition: background 0.2s;
}
.send-btn:hover { background: var(--maroon-hover); }

/* Markdown Overrides */
.ai-msg pre {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 16px;
    margin: 12px 0;
    overflow-x: auto;
}
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css_content)

print("✅ UI successfully reverted to the classic layout.")