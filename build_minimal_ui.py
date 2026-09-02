import os

# --- 1. HTML: OUR STRUCTURE, NEW VIBE ---
html_path = "frontend/index.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Siddique AI</title>
    <link rel="stylesheet" href="css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="app-layout">
        <!-- Sleek Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <span class="logo">>_ siddique-ai</span>
                <button id="new-chat-btn" class="icon-btn">＋</button>
            </div>
            <div class="history-list" id="history-list"></div>
            <div class="sidebar-footer">
                <span class="status-dot"></span> System Online
            </div>
        </aside>

        <!-- Main Chat Area -->
        <main class="main-content">
            <!-- Custom Hero Section -->
            <div class="hero-section" id="hero-section">
                <h1>Initialize workspace.</h1>
                <p>Hardware bridge, RAG memory, and live UI rendering active.</p>
                <div class="hero-suggestions">
                    <span>Try:</span>
                    <code>ping local hardware</code>
                    <code>render mobile checkout</code>
                </div>
            </div>

            <div class="chat-container" id="chat-container"></div>

            <!-- Floating Input -->
            <div class="input-wrapper">
                <div class="input-box">
                    <span class="attachment-icon" id="attach-btn" title="Attach Image">📎</span>
                    <textarea id="message-input" placeholder="Send a message..." rows="1"></textarea>
                    <button id="send-btn" class="send-action">↑</button>
                </div>
            </div>
        </main>
    </div>

    <input type="file" id="file-input" style="display: none;" accept="image/*">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="js/app.js"></script>
</body>
</html>
""")

# --- 2. CSS: MINIMALIST SKIN WITH MAROON ACCENTS ---
css_path = "frontend/css/style.css"
with open(css_path, "w", encoding="utf-8") as f:
    f.write("""
:root {
    --bg-deep: #09090b;       
    --bg-sidebar: #121214;    
    --bg-surface: #18181b;    
    --border-color: #27272a;  
    --text-main: #fafafa;     
    --text-muted: #a1a1aa;    
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

/* Sidebar */
.sidebar {
    width: 260px;
    background-color: var(--bg-sidebar);
    border-right: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
}
.sidebar-header {
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
}
.logo {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    color: var(--text-main);
}
.icon-btn {
    background: transparent;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    font-size: 18px;
    transition: color 0.2s;
}
.icon-btn:hover { color: var(--maroon-primary); }

.history-list {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
}
.history-item {
    padding: 10px 12px;
    margin-bottom: 4px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    color: var(--text-muted);
    transition: background 0.2s, color 0.2s;
}
.history-item:hover, .history-item.active {
    background: var(--bg-surface);
    color: var(--text-main);
}
.sidebar-footer {
    padding: 15px 20px;
    font-size: 12px;
    color: var(--text-muted);
    border-top: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    gap: 8px;
}
.status-dot {
    width: 8px;
    height: 8px;
    background-color: var(--maroon-primary);
    border-radius: 50%;
}

/* Main Content */
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
    top: 35%;
    text-align: left;
    max-width: 600px;
    width: 100%;
    padding: 0 20px;
    transition: opacity 0.3s ease;
}
.hero-section h1 {
    font-family: 'JetBrains Mono', monospace;
    font-size: 32px;
    margin-bottom: 12px;
}
.hero-section p {
    color: var(--text-muted);
    font-size: 15px;
    margin-bottom: 24px;
}
.hero-suggestions {
    display: flex;
    gap: 12px;
    align-items: center;
    font-size: 13px;
    color: var(--text-muted);
}
.hero-suggestions code {
    background: var(--bg-surface);
    padding: 4px 8px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    color: var(--text-main);
}

/* Chat Area */
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

/* Input Area */
.input-wrapper {
    position: absolute;
    bottom: 30px;
    width: 100%;
    max-width: 750px;
    padding: 0 20px;
    z-index: 20;
}
.input-box {
    display: flex;
    align-items: flex-end;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 10px 14px;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.input-box:focus-within {
    border-color: var(--maroon-primary);
    box-shadow: 0 0 0 1px var(--maroon-primary);
}
.attachment-icon {
    cursor: pointer;
    padding: 10px;
    color: var(--text-muted);
    transition: color 0.2s;
}
.attachment-icon:hover { color: var(--text-main); }

textarea {
    flex: 1;
    background: transparent;
    border: none;
    color: var(--text-main);
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    padding: 10px;
    resize: none;
    outline: none;
    max-height: 150px;
}
textarea::placeholder { color: var(--text-muted); }

.send-action {
    background: var(--maroon-primary);
    color: #fff;
    border: none;
    width: 32px;
    height: 32px;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 6px;
    margin-right: 4px;
    font-weight: bold;
    transition: background 0.2s;
}
.send-action:hover { background: var(--maroon-hover); }

/* Markdown Overrides */
.ai-msg pre {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 16px;
    margin: 12px 0;
    overflow-x: auto;
}
.ai-msg code { font-family: 'JetBrains Mono', monospace; font-size: 13px; }
""")

print("✅ UI updated: Minimalist typography with Siddique AI custom layout applied.")