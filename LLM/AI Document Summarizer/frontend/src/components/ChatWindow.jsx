// frontend/src/components/ChatWindow.jsx
import React, { useState } from 'react'

export default function ChatWindow({ history, onSend }) {
  const [input, setInput] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim()) {
      onSend(input)
      setInput('')
    }
  }

  return (
    <div>
      <div style={{ maxHeight: 300, overflowY: 'auto', margin: '10px 0' }}>
        {history.map((entry, idx) => (
          <div key={idx} style={{ marginBottom: 10 }}>
            <b>User:</b> {entry.question}<br />
            <b>AI:</b> {entry.answer}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          style={{ width: '80%' }}
        />
        <button type="submit">Ask</button>
      </form>
    </div>
  )
}

