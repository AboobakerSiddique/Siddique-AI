# 🧠 Siddique AI: Full-Stack Multimodal AI Agent

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

Siddique AI is a production-ready, highly contextual AI pair programmer and daily-driver agent built completely from scratch. 

Moving beyond standard API wrappers, this system operates as an **agentic workflow engine** powered by Google's Gemini 3.6 Flash model. It features a custom in-memory Retrieval-Augmented Generation (RAG) pipeline, real-time Server-Sent Events (SSE) streaming, local hardware IoT bridging, and a sandboxed Live UI component renderer.

---

## 🌍 Live Deployment

The application is deployed live using Render's cloud infrastructure:
* **Frontend Web Application:** [https://siddique-ai-frontend.onrender.com](https://siddique-ai-frontend.onrender.com)
* **Backend API (Swagger UI):** [https://siddique-ai.onrender.com/docs](https://siddique-ai.onrender.com/docs)

*(Note: The backend is hosted on Render's free tier. It may take 30-50 seconds to spin up from a cold start if it has been idle).*

---

## ✨ Complete Feature Breakdown

### 🤖 Core AI & Agentic Capabilities
* **Real-Time SSE Token Streaming:** Responses are streamed chunk-by-chunk using Server-Sent Events (SSE) to ensure ultra-low latency and a responsive, premium user experience.
* **Multimodal Vision Engine:** Users can drag-and-drop or upload images (PNG, JPEG, WebP). The UI dynamically encodes the payload into Base64 and pipes it to the Gemini vision engine. Ideal for debugging physical hardware wiring (e.g., veroboards), reviewing UI mockups, or analyzing architectural diagrams.
* **Custom Tool Registry (Function Calling):** The LLM is granted autonomous access to execute Python functions based on user intent, mapping natural language to executable backend code.

### 📚 Advanced Context & Memory
* **Custom RAG Vector Database:** A lightweight, pure-Python Retrieval-Augmented Generation pipeline. It uses Google's `text-embedding-004` model to convert local project documents (Markdown, TXT) into mathematical vectors, compares them using Cosine Similarity, and injects highly relevant contextual chunks directly into the AI's prompt.
* **Core Memory Extraction:** A background tool that allows the AI to explicitly "save" important user facts to a local persistent file, effectively bridging context across entirely separate chat sessions (circumventing standard LLM amnesia).
* **SQLite Persistence:** All chat histories, user authentication, and system logs are fully persisted via SQLAlchemy ORM mapping.

### 🔌 Developer & Hardware Tools
* **IoT Local Hardware Bridge:** The AI is equipped with an HTTPX-powered network tool capable of making GET/POST requests to local IP addresses. Users can instruct the AI to ping ESP32 microcontrollers, read gas sensor arrays, or diagnose hardware endpoints directly from the chat interface.
* **Live UI Component Rendering:** When the AI generates HTML/CSS (e.g., for a payment gateway mockup), the frontend automatically detects the Markdown code block, injects a sandboxed `iframe`, and live-compiles the code so the user can interact with the visual component immediately.
* **Web Scraping & File Reading:** The AI can autonomously read local backend directories or scrape external documentation URLs to answer highly specific technical questions.

### 🎨 UI/UX & Frontend Polish
* **Vanilla Architecture:** Built without bloated frameworks (No React/Vue). Pure, high-performance HTML5, CSS3, and JavaScript utilizing modern ES6+ features.
* **Premium Error Handling:** API rate limits or network disconnections trigger sleek, ChatGPT-style auto-dismissing toast notifications rather than breaking the chat UI.
* **Smooth Physics & Scrolling:** Engineered with `requestAnimationFrame` for buttery-smooth auto-scrolling during high-speed token generation.

---

## 🛠 Comprehensive Tech Stack

| Category | Technologies Used |
|----------|-------------------|
| **Backend** | Python 3.10, FastAPI, Uvicorn, Pydantic |
| **AI / ML** | Google GenAI SDK (Gemini 3.6 Flash, `text-embedding-004`) |
| **Database** | SQLite3, SQLAlchemy ORM, Custom JSON Vector DB |
| **Frontend** | HTML5, CSS3 (Custom Variables/Themes), Vanilla JS, Marked.js |
| **Networking**| Server-Sent Events (SSE), HTTPX, Base64 Encoding |
| **DevOps** | Docker, Docker Compose, Nginx, GitHub Actions (CI/CD) |

---

## 📂 System Architecture & Directory Structure

```text
siddique-ai/
│
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── llm/              # Gemini Client & Streaming Logic
│   │   ├── routes/           # API Endpoints (Auth, Chat, DB)
│   │   ├── tools/            # Agentic Tools (RAG, IoT, Memory, Scraper)
│   │   ├── database.py       # SQLAlchemy Connection Config
│   │   ├── main.py           # FastAPI Entry Point
│   │   ├── models.py         # SQLite Table Schemas
│   │   └── schemas.py        # Pydantic Data Validation Models
│   ├── docs/                 # Target folder for RAG document ingestion
│   ├── Dockerfile            # Backend Containerization
│   └── requirements.txt      # Python Dependencies
│
├── frontend/                 # Static Site Files
│   ├── css/
│   │   └── style.css         # Custom Dark Theme & UI Sandbox Styling
│   ├── js/
│   │   └── app.js            # SSE Client, DOM Manipulation, Toast Notifications
│   └── index.html            # Main Chat Interface
│
├── .github/workflows/        # Automated CI/CD Testing Pipeline
├── docker-compose.yml        # Multi-container Orchestration
├── LICENSE                   # MIT License
└── README.md                 # Project Documentation

```

---

## ⚙️ Installation & Local Deployment

### 1. Clone the Repository

```bash
git clone [https://github.com/AboobakerSiddique/siddique-ai.git](https://github.com/AboobakerSiddique/siddique-ai.git)
cd siddique-ai

```

### 2. Configure Environment Variables

Create a `.env` file in the `backend` directory and add your Google Gemini API key:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here

```

*(You must obtain an API key from Google AI Studio).*

### 3. Deploy via Docker (Recommended)

This project is fully containerized. To spin up the backend API, the SQLite database, and the Nginx frontend server in a single command:

```bash
docker-compose up --build

```

Once the containers are running, open your browser and navigate to: **`http://localhost:8080`**

### 4. Manual Setup (Without Docker)

If you prefer to run the environment manually:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

```

Then, simply open `frontend/index.html` in your web browser.

---

## 📌 API Reference

Explore the full interactive documentation at `/docs` (Swagger UI) when the server is running locally or in production.

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/auth/login` | Authenticates a user and returns a session state. |
| `GET` | `/conversations` | Retrieves all chat histories for the current user. |
| `POST` | `/conversations` | Initializes a new empty chat session. |
| `GET` | `/conversations/{id}` | Loads historical messages for a specific session ID. |
| `POST` | `/chat/stream` | Primary endpoint. Accepts text/images and streams SSE tokens. |

---

## 🚀 Future Roadmap

* [ ] **Voice Interaction:** Integrate WebSpeech API for real-time STT (Speech-to-Text) and TTS (Text-to-Speech).
* [ ] **OAuth2 Integration:** Add "Login with GitHub/Google" flows to replace manual authentication.
* [ ] **Cloud Vector DB Migration:** Upgrade the local in-memory JSON vector database to Pinecone or ChromaDB for massive scale.
* [ ] **Multi-Agent Reasoning:** Implement internal thought-loops where the AI verifies its own code output before streaming to the user.

---

## 👨‍💻 Author

**Aboobaker Siddique**

* GitHub: [@AboobakerSiddique](https://github.com/AboobakerSiddique)
* LinkedIn: [Aboobaker Siddique](https://www.google.com/search?q=https://www.linkedin.com/in/aboobaker-siddique-ba4a66333)

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for full details.

⭐ *If you found this project interesting or helpful, consider leaving a star on the repository!*

```

```