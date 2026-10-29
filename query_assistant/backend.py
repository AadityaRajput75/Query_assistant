from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import json
import uuid as uuid_module
from datetime import datetime
import asyncio

from backend_tools import restaurant_query_function
from session_manager import SessionManager

app = FastAPI(title="Restaurant Query Assistant API", version="1.0.0")

session_manager = SessionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    id: str
    message: str
    is_user: bool
    timestamp: datetime
    session_id: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    message_id: str
    timestamp: datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def read_root():
    return {"message": "Restaurant Query Assistant API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        session_id = request.session_id or str(uuid_module.uuid4())
        
        session_info = session_manager.get_session_info(session_id)
        is_new_session = session_info is None
        
        if is_new_session:
            session_manager.create_session(session_id, request.message)
        
        response_text = restaurant_query_function(request.message)
        
        response = ChatResponse(
            response=response_text,
            session_id=session_id,
            message_id=str(uuid_module.uuid4()),
            timestamp=datetime.now()
        )
        
        user_message_id = str(uuid_module.uuid4())
        session_manager.add_message(session_id, user_message_id, request.message, True)
        session_manager.add_message(session_id, response.message_id, response.response, False)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str):
    messages = session_manager.get_session_messages(session_id)
    return {"messages": messages}

@app.get("/sessions")
async def get_all_sessions():
    sessions = session_manager.get_all_sessions()
    return {"sessions": sessions}

@app.get("/sessions/{session_id}")
async def get_session_info(session_id: str):
    session_info = session_manager.get_session_info(session_id)
    if not session_info:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_info

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    deleted = session_manager.delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            user_message = message_data.get('message', '')
            
            if user_message:
                await manager.send_personal_message(
                    json.dumps({"type": "typing", "is_typing": True}), 
                    websocket
                )
                
                await asyncio.sleep(0.5)
                
                response_text = restaurant_query_function(user_message)
                
                session_info = session_manager.get_session_info(session_id)
                is_new_session = session_info is None
                
                if is_new_session:
                    session_manager.create_session(session_id, user_message)
                
                user_msg_id = str(uuid_module.uuid4())
                bot_msg_id = str(uuid_module.uuid4())
                
                session_manager.add_message(session_id, user_msg_id, user_message, True)
                session_manager.add_message(session_id, bot_msg_id, response_text, False)
                
                await manager.send_personal_message(
                    json.dumps({"type": "typing", "is_typing": False}), 
                    websocket
                )
                
                await manager.send_personal_message(
                    json.dumps({
                        "type": "message",
                        "id": bot_msg_id,
                        "message": response_text,
                        "is_user": False,
                        "timestamp": datetime.now().isoformat(),
                        "session_id": session_id
                    }), 
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=False)