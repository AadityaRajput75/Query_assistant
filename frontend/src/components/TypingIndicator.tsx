import React from 'react';

interface TypingIndicatorProps {
  isVisible: boolean;
}

const TypingIndicator: React.FC<TypingIndicatorProps> = ({ isVisible }) => {
  if (!isVisible) return null;

  return (
    <div className="flex items-start space-x-3 mb-4 animate-fade-in">
      <div className="flex-shrink-0 w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
        <span className="text-white text-sm font-medium">🤖</span>
      </div>
      <div className="chat-message bot-message p-3 rounded-lg shadow-sm">
        <div className="typing-indicator">
          <div className="typing-dot" style={{ animationDelay: '0s' }}></div>
          <div className="typing-dot" style={{ animationDelay: '0.2s' }}></div>
          <div className="typing-dot" style={{ animationDelay: '0.4s' }}></div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;