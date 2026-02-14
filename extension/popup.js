// Popup script for extension popup
// This handles the popup UI functionality

document.addEventListener('DOMContentLoaded', () => {
    // Check if backend is running
    checkBackendStatus();
});

async function checkBackendStatus() {
    try {
        const response = await fetch('http://localhost:5000/api/health');
        const data = await response.json();

        if (data.status === 'healthy') {
            updateStatus(true, 'Backend Connected');
        } else {
            updateStatus(false, 'Backend Error');
        }
    } catch (error) {
        updateStatus(false, 'Backend Offline');
    }
}

function updateStatus(isHealthy, message) {
    const statusDiv = document.querySelector('.status');
    const statusText = document.querySelector('.status-text');
    const statusDot = document.querySelector('.status-dot');

    if (isHealthy) {
        statusDiv.style.background = 'rgba(16, 185, 129, 0.2)';
        statusDiv.style.borderColor = 'rgba(16, 185, 129, 0.3)';
        statusText.style.color = '#6ee7b7';
        statusDot.style.background = '#10b981';
        statusText.textContent = message;
    } else {
        statusDiv.style.background = 'rgba(239, 68, 68, 0.2)';
        statusDiv.style.borderColor = 'rgba(239, 68, 68, 0.3)';
        statusText.style.color = '#fca5a5';
        statusDot.style.background = '#ef4444';
        statusDot.style.animation = 'none';
        statusText.textContent = message + ' - Start the Flask server';
    }
}
