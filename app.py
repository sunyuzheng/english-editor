from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="English Editor")

# Initialize OpenAI client with AI-builders-coach API
# Token will be checked when making API calls
def get_client():
    api_token = os.getenv("AI_BUILDER_TOKEN")
    if not api_token:
        raise ValueError("AI_BUILDER_TOKEN environment variable is not set. Please set it in your .env file or as an environment variable.")
    return OpenAI(
        base_url="https://space.ai-builders.com/resources/students-backend/v1",
        api_key=api_token
    )

# System prompt for English editing
SYSTEM_PROMPT = """Your role is to be an English guru, an expert in authentic American English, who assists users in expressing their thoughts clearly and fluently. You are not just translating words; you are delving into the essence of the user's message and reconstructing it in a way that maintains logical clarity and coherence. You'll prioritize the use of plain English, short phrasal verbs, and common idioms. It's important to craft sentences with varied lengths to create a natural rhythm and flow, making the language sound smooth and engaging. Avoid regional expressions or idioms that are too unique or restricted to specific areas. Your goal is to make American English accessible and appealing to a broad audience, helping users communicate effectively in a style that resonates with a wide range of English speakers. Avoid using hyphens when possible."""

class EditRequest(BaseModel):
    text: str

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    token_set = bool(os.getenv("AI_BUILDER_TOKEN"))
    return {
        "status": "healthy",
        "token_configured": token_set,
        "message": "Token is configured" if token_set else "Warning: AI_BUILDER_TOKEN not set",
        "version": "1.0.1",
        "last_updated": "2025-11-13T17:50:00"
    }

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>English Editor</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 16px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .header p {
                opacity: 0.9;
                font-size: 1.1em;
            }
            .content {
                padding: 40px;
            }
            .editor-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-bottom: 30px;
            }
            @media (max-width: 768px) {
                .editor-container {
                    grid-template-columns: 1fr;
                }
            }
            .editor-section {
                display: flex;
                flex-direction: column;
            }
            .editor-section label {
                font-weight: 600;
                margin-bottom: 10px;
                color: #333;
                font-size: 1.1em;
            }
            textarea {
                width: 100%;
                min-height: 400px;
                padding: 20px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 16px;
                font-family: inherit;
                resize: vertical;
                transition: border-color 0.3s;
            }
            textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            #output {
                background: #f8f9fa;
            }
            .button-container {
                display: flex;
                gap: 15px;
                justify-content: center;
            }
            button {
                padding: 15px 40px;
                font-size: 1.1em;
                font-weight: 600;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            #edit-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            #edit-btn:hover:not(:disabled) {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            }
            #edit-btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            #clear-btn {
                background: #6c757d;
                color: white;
            }
            #clear-btn:hover {
                background: #5a6268;
                transform: translateY(-2px);
            }
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
                color: #667eea;
                font-weight: 600;
            }
            .loading.show {
                display: block;
            }
            .spinner {
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 10px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✍️ English Editor</h1>
                <p>Transform your English text into polished, natural American English</p>
            </div>
            <div class="content">
                <div class="editor-container">
                    <div class="editor-section">
                        <label for="input">Your Text:</label>
                        <textarea id="input" placeholder="Paste your English text here..."></textarea>
                    </div>
                    <div class="editor-section">
                        <label for="output">Edited Text:</label>
                        <textarea id="output" placeholder="Your edited text will appear here..." readonly></textarea>
                    </div>
                </div>
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    Editing your text...
                </div>
                <div class="button-container">
                    <button id="edit-btn" onclick="editText()">Edit Text</button>
                    <button id="clear-btn" onclick="clearText()">Clear</button>
                </div>
            </div>
        </div>
        <script>
            async function editText() {
                const input = document.getElementById('input').value.trim();
                const output = document.getElementById('output');
                const editBtn = document.getElementById('edit-btn');
                const loading = document.getElementById('loading');
                
                if (!input) {
                    alert('Please enter some text to edit.');
                    return;
                }
                
                editBtn.disabled = true;
                loading.classList.add('show');
                output.value = '';
                
                try {
                    const response = await fetch('/edit', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ text: input })
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
                        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
                    }
                    
                    const data = await response.json();
                    if (!data.edited_text) {
                        throw new Error('No edited text returned from server');
                    }
                    output.value = data.edited_text;
                } catch (error) {
                    output.value = 'Error: ' + (error.message || 'Failed to edit text. Please try again.');
                    console.error('Edit error:', error);
                } finally {
                    editBtn.disabled = false;
                    loading.classList.remove('show');
                }
            }
            
            function clearText() {
                document.getElementById('input').value = '';
                document.getElementById('output').value = '';
            }
            
            // Allow Enter+Shift for new line, Enter alone submits
            document.getElementById('input').addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && e.ctrlKey) {
                    editText();
                }
            });
        </script>
    </body>
    </html>
    """

@app.post("/edit")
async def edit_text(request: EditRequest):
    try:
        client = get_client()
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Please edit and improve the following English text:\n\n{request.text}"}
            ],
            temperature=1.0,
            max_tokens=2048
        )
        
        if not response.choices or len(response.choices) == 0:
            raise ValueError("No response from API")
        
        edited_text = response.choices[0].message.content.strip()
        
        if not edited_text:
            raise ValueError("Empty response from API")
        
        return {"edited_text": edited_text}
    except ValueError as e:
        # Handle specific value errors
        raise HTTPException(status_code=500, detail=f"API Error: {str(e)}")
    except Exception as e:
        # Provide more detailed error information
        error_msg = str(e)
        error_type = type(e).__name__
        raise HTTPException(
            status_code=500, 
            detail=f"Error ({error_type}): {error_msg}. Please check if AI_BUILDER_TOKEN is set correctly."
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)

