from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot_engine import chat_with_video
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for Chrome extension


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    API endpoint for chatting with YouTube videos.
    
    Request JSON:
        {
            "video_id": "YouTube video ID",
            "question": "User's question"
        }
    
    Response JSON:
        {
            "answer": "AI-generated answer",
            "success": true
        }
        
        OR on error:
        {
            "error": "Error message",
            "success": false
        }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No JSON data provided",
                "success": False
            }), 400
        
        video_id = data.get('video_id')
        question = data.get('question')
        
        # Validate input
        if not video_id:
            return jsonify({
                "error": "video_id is required",
                "success": False
            }), 400
        
        if not question:
            return jsonify({
                "error": "question is required",
                "success": False
            }), 400
        
        # Get answer from chatbot
        answer = chat_with_video(video_id, question)
        
        return jsonify({
            "answer": answer,
            "success": True
        })
        
    except Exception as e:
        # Log the full traceback for debugging
        print("Error occurred:")
        traceback.print_exc()
        
        return jsonify({
            "error": str(e),
            "success": False
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "message": "YouTube Chatbot API is running"
    })


if __name__ == '__main__':
    print("🚀 Starting YouTube Chatbot API...")
    print("📡 Server running on http://localhost:5000")
    print("💡 Use POST /api/chat to ask questions about YouTube videos")
    app.run(debug=True, host='0.0.0.0', port=5000)
