# DocumentQA Integration Guide

## How to Integrate DocumentQA Chatbot into Your Website

### Step 1: Get Your API Key
1. Login to DocumentQA Dashboard
2. Go to **FAQs** tab
3. Copy your **API Key**

### Step 2: Add Chatbot Widget to Your Website

#### Option A: HTML/JavaScript (Recommended)

Add this to your website's `<body>` tag:

```html
<!-- DocumentQA Chatbot Widget -->
<div id="documentqa-chatbot"></div>

<script>
(function() {
  const API_KEY = 'YOUR_API_KEY_HERE';
  const BACKEND_URL = 'http://localhost:5000';
  
  const chatContainer = document.createElement('div');
  chatContainer.id = 'dqa-chat';
  chatContainer.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 400px;
    height: 500px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    display: flex;
    flex-direction: column;
    font-family: Arial, sans-serif;
    z-index: 9999;
  `;
  
  const header = document.createElement('div');
  header.style.cssText = `
    background: #6366f1;
    color: white;
    padding: 15px;
    border-radius: 10px 10px 0 0;
    font-weight: bold;
  `;
  header.textContent = 'MATW Support';
  
  const messagesDiv = document.createElement('div');
  messagesDiv.style.cssText = `
    flex: 1;
    overflow-y: auto;
    padding: 15px;
    background: #f9fafb;
  `;
  
  const inputDiv = document.createElement('div');
  inputDiv.style.cssText = `
    padding: 10px;
    border-top: 1px solid #e5e7eb;
    display: flex;
    gap: 10px;
  `;
  
  const input = document.createElement('input');
  input.type = 'text';
  input.placeholder = 'Ask a question...';
  input.style.cssText = `
    flex: 1;
    padding: 10px;
    border: 1px solid #d1d5db;
    border-radius: 5px;
    font-size: 14px;
  `;
  
  const sendBtn = document.createElement('button');
  sendBtn.textContent = 'Send';
  sendBtn.style.cssText = `
    padding: 10px 20px;
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
  `;
  
  chatContainer.appendChild(header);
  chatContainer.appendChild(messagesDiv);
  inputDiv.appendChild(input);
  inputDiv.appendChild(sendBtn);
  chatContainer.appendChild(inputDiv);
  document.body.appendChild(chatContainer);
  
  // Add message function
  function addMessage(text, isUser) {
    const msgDiv = document.createElement('div');
    msgDiv.style.cssText = `
      margin: 10px 0;
      padding: 10px;
      border-radius: 5px;
      background: ${isUser ? '#6366f1' : '#e5e7eb'};
      color: ${isUser ? 'white' : 'black'};
      word-wrap: break-word;
    `;
    msgDiv.textContent = text;
    messagesDiv.appendChild(msgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }
  
  // Send message
  sendBtn.onclick = async () => {
    const question = input.value.trim();
    if (!question) return;
    
    addMessage(question, true);
    input.value = '';
    
    try {
      const response = await fetch(`${BACKEND_URL}/api/chatbot/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          api_key: API_KEY,
          question: question,
          username: 'website-user',
          email: 'user@example.com'
        })
      });
      
      const data = await response.json();
      addMessage(data.answer, false);
    } catch (error) {
      addMessage('Error: Unable to connect to chatbot', false);
    }
  };
  
  input.onkeypress = (e) => {
    if (e.key === 'Enter') sendBtn.click();
  };
})();
</script>
```

#### Option B: React Component

```jsx
import React, { useState } from 'react';

export function DocumentQAChatbot({ apiKey, backendUrl = 'http://localhost:5000' }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  
  const sendMessage = async () => {
    if (!input.trim()) return;
    
    setMessages([...messages, { text: input, isUser: true }]);
    setInput('');
    
    try {
      const response = await fetch(`${backendUrl}/api/chatbot/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          api_key: apiKey,
          question: input,
          username: 'website-user',
          email: 'user@example.com'
        })
      });
      
      const data = await response.json();
      setMessages(prev => [...prev, { text: data.answer, isUser: false }]);
    } catch (error) {
      setMessages(prev => [...prev, { text: 'Error connecting to chatbot', isUser: false }]);
    }
  };
  
  return (
    <div style={{ width: '400px', height: '500px', border: '1px solid #ddd', borderRadius: '10px', display: 'flex', flexDirection: 'column' }}>
      <div style={{ background: '#6366f1', color: 'white', padding: '15px', borderRadius: '10px 10px 0 0' }}>
        MATW Support
      </div>
      <div style={{ flex: 1, overflow: 'auto', padding: '15px', background: '#f9fafb' }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ margin: '10px 0', padding: '10px', borderRadius: '5px', background: msg.isUser ? '#6366f1' : '#e5e7eb', color: msg.isUser ? 'white' : 'black' }}>
            {msg.text}
          </div>
        ))}
      </div>
      <div style={{ padding: '10px', borderTop: '1px solid #e5e7eb', display: 'flex', gap: '10px' }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask a question..."
          style={{ flex: 1, padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px' }}
        />
        <button onClick={sendMessage} style={{ padding: '10px 20px', background: '#6366f1', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
          Send
        </button>
      </div>
    </div>
  );
}
```

### Step 3: Customize FAQs

1. In DocumentQA Dashboard, go to **FAQs** tab
2. Add your website/organization FAQs
3. Upload PDFs with knowledge base
4. Chatbot will automatically answer user questions

### Step 4: Deploy Backend (Optional)

For production, deploy backend to AWS/Heroku:

```bash
# Heroku example
heroku login
heroku create your-app-name
git push heroku main
```

---

## API Endpoint

**POST** `/api/chatbot/ask`

**Request:**
```json
{
  "api_key": "YOUR_API_KEY",
  "question": "What is MATW?",
  "username": "user123",
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "answer": "MATW is a charity organization...",
  "confidence": 0.95,
  "source": "faq",
  "conversation_id": "uuid"
}
```

---

## Support

For issues, email: support@matw.com

