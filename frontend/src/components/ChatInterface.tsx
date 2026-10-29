import React, { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Menu, MessageCircle } from 'lucide-react';
import MessageBubble from './MessageBubble';
import MessageInput from './MessageInput';
import TypingIndicator from './TypingIndicator';
import SessionSidebar from './SessionSidebar';
import { ChatMessage, WebSocketMessage } from '../types/chat';
import { chatService } from '../services/api';

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState(() => uuidv4());
  const [websocket, setWebsocket] = useState<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [connectionError, setConnectionError] = useState<string | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [currentSessionName, setCurrentSessionName] = useState<string>('New Chat');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadSessionMessages = async (sessionId: string) => {
    try {
      const response = await chatService.getSessionMessages(sessionId);
      const sessionMessages = response.messages.map((msg: any) => ({
        id: msg.id,
        message: msg.message,
        isUser: msg.isUser,
        timestamp: new Date(msg.timestamp),
        sessionId: msg.sessionId,
      }));
      setMessages(sessionMessages);
    } catch (error) {
      console.error('Error loading session messages:', error);
      setMessages([]);
    }
  };

  const loadSessionInfo = async (sessionId: string) => {
    try {
      const sessionInfo = await chatService.getSessionInfo(sessionId);
      setCurrentSessionName(sessionInfo.name || 'Chat Session');
    } catch (error) {
      console.error('Error loading session info:', error);
      setCurrentSessionName('Chat Session');
    }
  };

  const handleSessionSelect = async (newSessionId: string) => {
    if (newSessionId === sessionId) return;
    
    if (websocket) {
      websocket.close();
      setWebsocket(null);
    }
    
    setSessionId(newSessionId);
    setMessages([]);
    setIsTyping(false);
    
    await loadSessionMessages(newSessionId);
    await loadSessionInfo(newSessionId);
  };

  const handleNewSession = () => {
    if (websocket) {
      websocket.close();
      setWebsocket(null);
    }
    
    const newSessionId = uuidv4();
    setSessionId(newSessionId);
    setMessages([]);
    setIsTyping(false);
    setCurrentSessionName('New Chat');
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    const loadExistingSession = async () => {
      try {
        await loadSessionInfo(sessionId);
        await loadSessionMessages(sessionId);
      } catch (error) {
        console.log('New session created');
      }
    };
    
    loadExistingSession();
  }, []);

  // WebSocket connection
  useEffect(() => {
    const connectWebSocket = () => {
        const ws = new WebSocket(`ws://localhost:8001/ws/${sessionId}`);      ws.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
        setConnectionError(null);
      };

      ws.onmessage = (event) => {
        const data: WebSocketMessage = JSON.parse(event.data);
        
        if (data.type === 'typing') {
          setIsTyping(data.is_typing || false);
        } else if (data.type === 'message' && !data.is_user) {
          const newMessage: ChatMessage = {
            id: data.id || uuidv4(),
            message: data.message || '',
            isUser: false,
            timestamp: data.timestamp ? new Date(data.timestamp) : new Date(),
            sessionId: data.session_id,
          };
          setMessages(prev => [...prev, newMessage]);
        }
      };

      ws.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason);
        setIsConnected(false);
        
        if (event.code !== 1000) {
          setTimeout(() => {
            console.log('Attempting to reconnect...');
            connectWebSocket();
          }, 3000);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionError('Connection failed. Using REST API fallback.');
      };

      setWebsocket(ws);
    };

    connectWebSocket();

    return () => {
      websocket?.close(1000, 'Component unmounting');
    };
  }, [sessionId]);

  const sendMessage = async (messageText: string) => {
    const userMessage: ChatMessage = {
      id: uuidv4(),
      message: messageText,
      isUser: true,
      timestamp: new Date(),
      sessionId,
    };

    setMessages(prev => [...prev, userMessage]);

    if (websocket && websocket.readyState === WebSocket.OPEN) {
      websocket.send(JSON.stringify({ message: messageText }));
    } else {
      setIsTyping(true);
      try {
        const response = await chatService.sendMessage({
          message: messageText,
          session_id: sessionId,
        });

        const botMessage: ChatMessage = {
          id: response.message_id,
          message: response.response,
          isUser: false,
          timestamp: new Date(response.timestamp),
          sessionId: response.session_id,
        };

        setMessages(prev => [...prev, botMessage]);
      } catch (error) {
        console.error('Error sending message:', error);
        const errorMessage: ChatMessage = {
          id: uuidv4(),
          message: 'Sorry, I encountered an error. Please try again.',
          isUser: false,
          timestamp: new Date(),
          sessionId,
        };
        setMessages(prev => [...prev, errorMessage]);
      } finally {
        setIsTyping(false);
      }
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setIsSidebarOpen(true)}
              className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
            >
              <Menu size={20} />
            </button>
            <div>
              <div className="flex items-center space-x-2">
                <MessageCircle size={20} className="text-primary-500" />
                <h1 className="text-xl font-semibold text-gray-900">{currentSessionName}</h1>
              </div>
              <p className="text-sm text-gray-500">Ask me anything about restaurants!</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-xs text-gray-500">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </div>
        {connectionError && (
          <div className="mt-2 text-xs text-amber-600 bg-amber-50 px-2 py-1 rounded">
            {connectionError}
          </div>
        )}
      </div>

      <div className="flex-1 overflow-y-auto px-6 py-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="text-6xl mb-4">🍽️</div>
            <h2 className="text-xl font-semibold text-gray-700 mb-2">Welcome to Restaurant Assistant!</h2>
            <p className="text-gray-500 max-w-md">
              I can help you find restaurants, cafes, buffets, and more. Try asking about:
            </p>
            <ul className="text-sm text-gray-400 mt-3 space-y-1">
              <li>• "Show me all cafes"</li>
              <li>• "Find cheap restaurants"</li>
              <li>• "Best rated restaurants"</li>
              <li>• "Restaurants with online ordering"</li>
            </ul>
          </div>
        )}
        
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        
        <TypingIndicator isVisible={isTyping} />
        <div ref={messagesEndRef} />
      </div>

      <MessageInput 
        onSendMessage={sendMessage}
        disabled={isTyping}
        placeholder="Ask about restaurants, cafes, or food places..."
      />

      <SessionSidebar
        currentSessionId={sessionId}
        onSessionSelect={handleSessionSelect}
        onNewSession={handleNewSession}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
      />
    </div>
  );
};

export default ChatInterface;