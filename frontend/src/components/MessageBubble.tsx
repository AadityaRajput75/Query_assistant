import React from 'react';
import ReactMarkdown from 'react-markdown';
import { ChatMessage } from '../types/chat';

interface MessageBubbleProps {
  message: ChatMessage;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const formatTime = (timestamp: Date) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`flex items-start space-x-3 mb-4 animate-slide-up ${message.isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        message.isUser 
          ? 'bg-gray-300 text-gray-700' 
          : 'bg-primary-500 text-white'
      }`}>
        <span className="text-sm font-medium">
          {message.isUser ? '👤' : '🤖'}
        </span>
      </div>
      
      <div className={`chat-message p-3 rounded-lg shadow-sm ${
        message.isUser ? 'user-message' : 'bot-message'
      }`}>
        <div className="markdown-content">
          {message.isUser ? (
            <p className="text-sm leading-relaxed">{message.message}</p>
          ) : (
            <ReactMarkdown 
              className="text-sm"
              components={{
                p: ({ children }) => <p className="mb-2 last:mb-0 leading-relaxed">{children}</p>,
                strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
                em: ({ children }) => <em className="italic">{children}</em>,
                ul: ({ children }) => <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>,
                ol: ({ children }) => <ol className="list-decimal list-inside mb-2 space-y-1">{children}</ol>,
                li: ({ children }) => <li className="text-sm">{children}</li>,
                h1: ({ children }) => <h1 className="text-lg font-bold mb-2">{children}</h1>,
                h2: ({ children }) => <h2 className="text-base font-bold mb-2">{children}</h2>,
                h3: ({ children }) => <h3 className="text-sm font-bold mb-2">{children}</h3>,
                code: ({ children }) => <code className="bg-gray-100 px-1 py-0.5 rounded text-xs font-mono">{children}</code>,
              }}
            >
              {message.message}
            </ReactMarkdown>
          )}
        </div>
        <div className={`text-xs mt-2 opacity-70 ${message.isUser ? 'text-white' : 'text-gray-500'}`}>
          {formatTime(message.timestamp)}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;