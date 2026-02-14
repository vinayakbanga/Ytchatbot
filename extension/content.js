// Content script for YouTube pages
// This script injects the chatbot sidebar into YouTube video pages

const API_URL = 'http://localhost:5000/api/chat';

let chatSidebar = null;
let messagesContainer = null;
let inputField = null;
let sendButton = null;
let isOpen = false;

// Extract video ID from YouTube URL
function getVideoId() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('v');
}

// Create the chat sidebar UI
function createChatSidebar() {
    // Main sidebar container
    chatSidebar = document.createElement('div');
    chatSidebar.className = 'yt-chatbot-sidebar hidden';

    // Header
    const header = document.createElement('div');
    header.className = 'yt-chatbot-header';
    header.innerHTML = `
        <h2 class="yt-chatbot-title">💬 Video Chat AI</h2>
        <button class="yt-chatbot-close">×</button>
    `;

    // Messages container
    messagesContainer = document.createElement('div');
    messagesContainer.className = 'yt-chatbot-messages';
    messagesContainer.innerHTML = `
        <div class="yt-chatbot-welcome">
            <div class="yt-chatbot-welcome-icon">🤖</div>
            <div class="yt-chatbot-welcome-text">
                Hi! I'm your AI assistant.<br>
                Ask me anything about this video!
            </div>
        </div>
    `;

    // Input container
    const inputContainer = document.createElement('div');
    inputContainer.className = 'yt-chatbot-input-container';
    inputContainer.innerHTML = `
        <div class="yt-chatbot-input-wrapper">
            <input 
                type="text" 
                class="yt-chatbot-input" 
                placeholder="Ask a question about this video..."
                maxlength="500"
            />
            <button class="yt-chatbot-send">➤</button>
        </div>
    `;

    // Assemble sidebar
    chatSidebar.appendChild(header);
    chatSidebar.appendChild(messagesContainer);
    chatSidebar.appendChild(inputContainer);

    // Add to page
    document.body.appendChild(chatSidebar);

    // Get references
    inputField = inputContainer.querySelector('.yt-chatbot-input');
    sendButton = inputContainer.querySelector('.yt-chatbot-send');
    const closeButton = header.querySelector('.yt-chatbot-close');

    // Event listeners
    closeButton.addEventListener('click', toggleSidebar);
    sendButton.addEventListener('click', sendMessage);
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

// Create toggle button
function createToggleButton() {
    const toggleButton = document.createElement('button');
    toggleButton.className = 'yt-chatbot-toggle';
    toggleButton.innerHTML = '💬';
    toggleButton.addEventListener('click', toggleSidebar);
    document.body.appendChild(toggleButton);
    console.log('✅ Chat toggle button created and added to page!');
    console.log('📍 Button element:', toggleButton);
    console.log('🎨 Button should be visible in bottom-right corner');
}

// Toggle sidebar visibility
function toggleSidebar() {
    isOpen = !isOpen;
    if (isOpen) {
        chatSidebar.classList.remove('hidden');
    } else {
        chatSidebar.classList.add('hidden');
    }
}

// Format text with markdown-like syntax
function formatText(text) {
    // Convert **bold** to <strong>
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // Convert *italic* to <em>
    text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // Convert bullet points (- item or * item) to proper list items
    const lines = text.split('\n');
    let formattedLines = [];
    let inList = false;

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();

        // Check for bullet points
        if (line.match(/^[-*]\s+(.+)/)) {
            if (!inList) {
                formattedLines.push('<ul>');
                inList = true;
            }
            const content = line.replace(/^[-*]\s+/, '');
            formattedLines.push(`<li>${content}</li>`);
        }
        // Check for numbered lists
        else if (line.match(/^\d+\.\s+(.+)/)) {
            if (!inList) {
                formattedLines.push('<ol>');
                inList = true;
            }
            const content = line.replace(/^\d+\.\s+/, '');
            formattedLines.push(`<li>${content}</li>`);
        }
        else {
            if (inList) {
                formattedLines.push('</ul>');
                inList = false;
            }
            if (line) {
                formattedLines.push(`<p>${line}</p>`);
            }
        }
    }

    if (inList) {
        formattedLines.push('</ul>');
    }

    return formattedLines.join('');
}

// Add message to chat
function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `yt-chatbot-message ${isUser ? 'user' : 'bot'}`;

    const avatar = document.createElement('div');
    avatar.className = 'yt-chatbot-avatar';
    avatar.textContent = isUser ? '👤' : '🤖';

    const bubble = document.createElement('div');
    bubble.className = 'yt-chatbot-bubble';

    // Use formatted HTML for bot messages, plain text for user messages
    if (isUser) {
        bubble.textContent = text;
    } else {
        bubble.innerHTML = formatText(text);
    }

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);

    // Remove welcome message if it exists
    const welcome = messagesContainer.querySelector('.yt-chatbot-welcome');
    if (welcome) {
        welcome.remove();
    }

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Show loading indicator
function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'yt-chatbot-message bot';
    loadingDiv.id = 'loading-indicator';

    const avatar = document.createElement('div');
    avatar.className = 'yt-chatbot-avatar';
    avatar.textContent = '🤖';

    const bubble = document.createElement('div');
    bubble.className = 'yt-chatbot-bubble';
    bubble.innerHTML = `
        <div class="yt-chatbot-loading">
            <div class="yt-chatbot-loading-dot"></div>
            <div class="yt-chatbot-loading-dot"></div>
            <div class="yt-chatbot-loading-dot"></div>
        </div>
    `;

    loadingDiv.appendChild(avatar);
    loadingDiv.appendChild(bubble);
    messagesContainer.appendChild(loadingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Remove loading indicator
function hideLoading() {
    const loading = document.getElementById('loading-indicator');
    if (loading) {
        loading.remove();
    }
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'yt-chatbot-error';
    errorDiv.textContent = `⚠️ ${message}`;

    const inputContainer = chatSidebar.querySelector('.yt-chatbot-input-container');
    chatSidebar.insertBefore(errorDiv, inputContainer);

    // Remove error after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Send message to backend
async function sendMessage() {
    const question = inputField.value.trim();

    if (!question) {
        return;
    }

    const videoId = getVideoId();
    if (!videoId) {
        showError('No video detected. Please open a YouTube video.');
        return;
    }

    // Add user message
    addMessage(question, true);
    inputField.value = '';

    // Disable input while processing
    inputField.disabled = true;
    sendButton.disabled = true;

    // Show loading
    showLoading();

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                video_id: videoId,
                question: question
            })
        });

        const data = await response.json();

        hideLoading();

        if (data.success) {
            addMessage(data.answer, false);
        } else {
            showError(data.error || 'Failed to get answer');
        }
    } catch (error) {
        hideLoading();
        console.error('Error:', error);
        showError('Cannot connect to backend. Make sure the API server is running.');
    } finally {
        // Re-enable input
        inputField.disabled = false;
        sendButton.disabled = false;
        inputField.focus();
    }
}

// Initialize when page loads
function init() {
    // Only run on video pages
    if (!getVideoId()) {
        console.log('⚠️ Not a video page, extension not initialized');
        return;
    }

    console.log('🚀 Initializing YouTube Chatbot extension...');
    console.log('📹 Video ID detected:', getVideoId());

    createChatSidebar();
    createToggleButton();

    console.log('✅ YouTube Chatbot extension loaded!');
    console.log('💡 Look for the 💬 button in the bottom-right corner!');
}

// Wait for page to load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Re-initialize when navigating to a new video (YouTube is a SPA)
let lastVideoId = getVideoId();
setInterval(() => {
    const currentVideoId = getVideoId();
    if (currentVideoId && currentVideoId !== lastVideoId) {
        lastVideoId = currentVideoId;
        // Clear messages when video changes
        if (messagesContainer) {
            messagesContainer.innerHTML = `
                <div class="yt-chatbot-welcome">
                    <div class="yt-chatbot-welcome-icon">🤖</div>
                    <div class="yt-chatbot-welcome-text">
                        Hi! I'm your AI assistant.<br>
                        Ask me anything about this video!
                    </div>
                </div>
            `;
        }
    }
}, 1000);
