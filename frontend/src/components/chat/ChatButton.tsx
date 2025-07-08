import React, { useState } from 'react';
import { Bot } from 'lucide-react';
import ChatWindow from './ChatWindow';

const ChatButton: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 bg-blue-500 hover:bg-blue-600 text-white rounded-full p-3 shadow-lg transition-transform hover:scale-110"
        aria-label="Open chat"
      >
        <Bot className="w-6 h-6" />
      </button>
      
      {isOpen && <ChatWindow onClose={() => setIsOpen(false)} />}
    </>
  );
};

export default ChatButton;