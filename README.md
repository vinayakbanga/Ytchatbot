# YouTube Video Chatbot - Chrome Extension

A Chrome extension that lets you ask questions about YouTube videos using AI-powered chatbot technology. Built with LangChain, HuggingFace, and Flask.

## 🌟 Features

- 💬 **Chat with YouTube Videos**: Ask questions about any YouTube video's content
- 🤖 **AI-Powered**: Uses HuggingFace's Gemma model for intelligent responses
- 🎨 **Modern UI**: Beautiful glassmorphism design with smooth animations
- ⚡ **Real-time**: Get instant answers while watching videos
- 🔒 **Privacy-Focused**: All processing happens through your own API server

## 📋 Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- HuggingFace API key ([Get one here](https://huggingface.co/settings/tokens))

## 🚀 Setup Instructions

### 1. Backend Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd c:\Users\Vinayak Banga\Desktop\Ytchatbotchromeext
   ```

2. **Create and activate virtual environment** (if not already done):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the project root
   - Add your HuggingFace API key:
     ```
     HUGGINGFACE_API_KEY=your_api_key_here
     ```

5. **Start the Flask API server:**
   ```bash
   python app.py
   ```
   
   You should see:
   ```
   🚀 Starting YouTube Chatbot API...
   📡 Server running on http://localhost:5000
   ```

### 2. Chrome Extension Setup

1. **Open Chrome and navigate to:**
   ```
   chrome://extensions/
   ```

2. **Enable "Developer mode"** (toggle in top-right corner)

3. **Click "Load unpacked"**

4. **Select the extension folder:**
   ```
   c:\Users\Vinayak Banga\Desktop\Ytchatbotchromeext\extension
   ```

5. **The extension should now appear in your extensions list!**

## 📖 How to Use

1. **Start the backend server** (if not already running):
   ```bash
   python app.py
   ```

2. **Open any YouTube video** in Chrome

3. **Click the chat button (💬)** in the bottom-right corner of the page

4. **Ask questions** about the video content in the chat sidebar

5. **Get AI-powered answers** instantly!

### Example Questions:
- "What is this video about?"
- "Summarize the main points"
- "What does the speaker say about [topic]?"
- "Can you explain [specific concept] mentioned in the video?"

## 🏗️ Project Structure

```
Ytchatbotchromeext/
├── app.py                  # Flask API server
├── chatbot_engine.py       # Core chatbot logic
├── chatbotbackend.py       # Original backend script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API keys)
├── extension/              # Chrome extension files
│   ├── manifest.json       # Extension configuration
│   ├── content.js          # Content script (injected into YouTube)
│   ├── styles.css          # Extension styling
│   ├── popup.html          # Extension popup UI
│   ├── popup.js            # Popup functionality
│   └── icon*.png           # Extension icons
└── venv/                   # Virtual environment
```

## 🔐 Security Features

- **Prompt Injection Detection**: Robust regex-based blocklist to identify and neutralize malicious instructions.
- **Context Leakage Prevention**: Prevents the LLM from dumping internal transcript data or system prompts.
- **Output Guardrails**: Enforces English-only responses and strict adherence to provided context.
- **Input Sanitization**: Pre-processes user queries to strip common attack patterns.
- **Secure Prompt Design**: Uses XML-style delimiters (`<user_question>`) and hardened system instructions to separate data from commands.
- **SAST (Static Analysis)**: Regular scanning with Semgrep to ensure code safety and best practices.

## 🧪 Security Testing

- **Performed DAST**: Manual attack testing against the live Flask API endpoints.
- **Jailbreak Testing**: Validated defenses against "ignore previous instructions" and system prompt extraction attacks.
- **Compliance**: Verified against OWASP Top 10 security standards using specialized Semgrep rules.

## 🛠️ Technical Details

### Backend Stack:
- **Flask**: REST API server
- **LangChain**: RAG (Retrieval-Augmented Generation) framework
- **HuggingFace**: LLM provider (Gemma-3-27b-it model)
- **FAISS**: Vector database for semantic search
- **YouTube Transcript API**: Fetch video transcripts

### Frontend Stack:
- **Vanilla JavaScript**: Extension logic
- **CSS3**: Modern glassmorphism design
- **Chrome Extension API**: Browser integration

### How It Works:
1. Extension detects YouTube video ID from URL
2. User asks a question via the chat interface
3. Question is sent to Flask API (`/api/chat`)
4. Backend fetches video transcript (cached for performance)
5. Transcript is split into chunks and embedded
6. Relevant chunks are retrieved using semantic search
7. LLM generates answer based on retrieved context
8. Answer is displayed in the chat interface

## 🔧 Configuration

### Change API Endpoint:
Edit `API_URL` in `extension/content.js`:
```javascript
const API_URL = 'http://localhost:5000/api/chat';
```

### Change LLM Model:
Edit `chatbot_engine.py`:
```python
llm = HuggingFaceEndpoint(
    repo_id="google/gemma-3-27b-it",  # Change this
    # ...
)
```

## 🐛 Troubleshooting

### "Cannot connect to backend" error:
- Make sure Flask server is running (`python app.py`)
- Check that server is on `http://localhost:5000`
- Verify no firewall is blocking the connection

### "Transcripts are disabled" error:
- Some videos don't have transcripts available
- Try a different video with captions enabled

### Extension not appearing:
- Make sure Developer mode is enabled in Chrome
- Check for errors in `chrome://extensions/`
- Try reloading the extension

### Import errors in VS Code:
- Select the correct Python interpreter: `.\venv\Scripts\python.exe`
- Press `Ctrl+Shift+P` → "Python: Select Interpreter"

## 📝 Notes

- The first question for each video may take longer (fetching transcript + creating embeddings)
- Subsequent questions are faster due to caching
- The extension only works on YouTube video pages
- Make sure you have a stable internet connection for API calls

## 🎨 Customization

The extension uses a modern dark theme with purple/blue gradients. To customize:

- **Colors**: Edit CSS variables in `extension/styles.css`
- **Layout**: Modify sidebar width and positioning in `styles.css`
- **Icons**: Replace `icon*.png` files in the extension folder

## 📄 License

This project is for educational purposes.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Powered by [HuggingFace](https://huggingface.co/)
- Uses [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)

---

**Enjoy chatting with YouTube videos! 💬🎥**
