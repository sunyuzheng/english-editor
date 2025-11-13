# English Editor

A simple web-based English editor that uses GPT-5 via AI-builders-coach API to improve and polish English text.

## Features

- Clean, modern web interface
- Real-time text editing using GPT-5
- Focuses on natural American English
- Simple and easy to use

## Setup

1. Install dependencies (creates virtual environment automatically):
```bash
cd english_editor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Get your AI_BUILDER_TOKEN:
   - The token is available through the AI-builders-coach MCP
   - Or check your environment variables if already set

3. Set your AI_BUILDER_TOKEN:

   **Option A: Create a `.env` file** (recommended):
   ```bash
   echo "AI_BUILDER_TOKEN=your_token_here" > .env
   ```

   **Option B: Export as environment variable**:
   ```bash
   export AI_BUILDER_TOKEN=your_token_here
   ```

4. Run the application:

   **Easy way** (uses start.sh script):
   ```bash
   ./start.sh
   ```

   **Manual way**:
   ```bash
   source venv/bin/activate
   python app.py
   ```

   Or using uvicorn directly:
   ```bash
   source venv/bin/activate
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

5. Open your browser and navigate to:
```
http://localhost:8000
```

**Note**: The server will start even without the token, but you'll need to set it before using the editor functionality.

## Usage

1. Paste your English text in the left textarea
2. Click "Edit Text" button
3. The improved text will appear in the right textarea
4. Use "Clear" to reset both textareas

## API Endpoint

You can also use the API directly:

```bash
curl -X POST "http://localhost:8000/edit" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here"}'
```

