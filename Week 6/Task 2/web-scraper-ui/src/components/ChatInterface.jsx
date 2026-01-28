import { useState, useRef, useEffect } from 'react';
import { crawlWebContent, resetSession } from '../services/api';
import './ChatInterface.css';

function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = {
      type: 'user',
      content: input,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const result = await crawlWebContent(input);
      
      const botMessage = {
        type: 'bot',
        content: result.content || JSON.stringify(result, null, 2),
        timestamp: new Date().toLocaleTimeString(),
        success: !!result.content,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        type: 'bot',
        content: `Error: ${error.message}`,
        timestamp: new Date().toLocaleTimeString(),
        success: false,
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setMessages([]);
    resetSession(); // Start a new Bedrock agent session
  };

  return (
    <div className="chat-interface">
      <div className="messages-container">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h2>👋 Welcome!</h2>
            <p>Ask me anything and I'll scrape the web for information.</p>
            {/* <div className="example-queries">
              <p>Try asking:</p>
              <ul>
                <li>"What is React?"</li>
                <li>"Latest news about AI"</li>
                <li>"AWS Lambda features"</li>
              </ul>
            </div> */}
          </div>
        )}

        {messages.map((message, index) => (
          <div key={index} className={`message ${message.type}`}>
            <div className="message-header">
              <span className="message-sender">
                {message.type === 'user' ? '👤 You' : '🤖 AI Agent'}
              </span>
              <span className="message-time">{message.timestamp}</span>
            </div>
            <div className="message-content">
              {message.content}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message bot loading">
            <div className="message-header">
              <span className="message-sender">🤖 AI Agent</span>
            </div>
            <div className="message-content">
              <div className="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        {messages.length > 0 && (
          <button
            type="button"
            onClick={handleClear}
            className="clear-button"
            title="Clear chat"
          >
            🗑️
          </button>
        )}
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question to scrape the web..."
          className="message-input"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="send-button"
          disabled={!input.trim() || isLoading}
        >
          {isLoading ? '⏳' : '🚀'}
        </button>
      </form>
    </div>
  );
}

export default ChatInterface;
