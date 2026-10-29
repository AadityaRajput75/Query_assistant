# Restaurant Query Assistant - React Frontend

A modern React-based chat interface for the Restaurant Query Assistant, replacing the Google ADK web interface.

## Features

- **Modern React Frontend**: Built with TypeScript, Tailwind CSS, and modern React hooks
- **Real-time Chat**: WebSocket support with REST API fallback
- **Responsive Design**: Works on desktop and mobile devices
- **Rich Message Formatting**: Markdown support for restaurant data display
- **Typing Indicators**: Visual feedback when the assistant is processing
- **Connection Status**: Real-time connection status indicator

## Quick Start

1. **Start Everything**: Run the main startup script
   ```cmd
   start_react.bat
   ```

2. **Access the Application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Manual Setup

### Backend (FastAPI)

1. Install Python dependencies:
   ```cmd
   cd query_assistant
   pip install -r requirements.txt
   ```

2. Start the database:
   ```cmd
   docker-compose up -d
   ```

3. Load the restaurant data:
   ```cmd
   python load_data.py
   ```

4. Start the FastAPI server:
   ```cmd
   python -m uvicorn backend:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend (React)

1. Install Node.js dependencies:
   ```cmd
   cd frontend
   npm install
   ```

2. Start the development server:
   ```cmd
   npm run dev
   ```

## API Endpoints

- `POST /chat` - Send a message and get a response
- `GET /sessions/{session_id}/messages` - Get message history
- `WS /ws/{session_id}` - WebSocket connection for real-time chat
- `GET /health` - Health check endpoint

## Project Structure

```
├── query_assistant/
│   ├── backend.py          # FastAPI server
│   ├── tools.py           # Restaurant query functions
│   ├── agent.py           # Original ADK agent (now unused)
│   ├── requirements.txt   # Python dependencies
│   └── ...
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── types/         # TypeScript type definitions
│   │   ├── services/      # API service layer
│   │   └── ...
│   ├── package.json       # Node.js dependencies
│   └── ...
└── start_react.bat        # Main startup script
```

## Architecture

The new architecture replaces Google ADK with:

1. **FastAPI Backend**: Wraps the existing restaurant query logic in REST API and WebSocket endpoints
2. **React Frontend**: Modern chat interface with TypeScript and Tailwind CSS
3. **WebSocket Communication**: Real-time bidirectional communication with REST fallback
4. **Session Management**: In-memory session storage for chat history

## Usage Examples

Try these queries in the chat interface:

- "Show me all cafes"
- "Find cheap restaurants"
- "Best rated restaurants"
- "Restaurants with online ordering"
- "All buffet restaurants"
- "Most expensive restaurants"

## Development

### Frontend Development
```cmd
cd frontend
npm run dev    # Start dev server
npm run build  # Build for production
npm run lint   # Run linter
```

### Backend Development
```cmd
cd query_assistant
python -m uvicorn backend:app --reload  # Start with auto-reload
```

The backend includes:
- Automatic API documentation at `/docs`
- CORS support for frontend development
- WebSocket and REST API endpoints
- Session management
- Error handling and logging