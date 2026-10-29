export interface ChatMessage {
  id: string;
  message: string;
  isUser: boolean;
  timestamp: Date;
  sessionId?: string;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  message_id: string;
  timestamp: string;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
}

export interface WebSocketMessage {
  type: 'message' | 'typing' | 'error';
  id?: string;
  message?: string;
  is_user?: boolean;
  timestamp?: string;
  session_id?: string;
  is_typing?: boolean;
}