// frontend/src/App.jsx
import React, { useState } from 'react'
import axios from 'axios'
import ChatWindow from './components/ChatWindow'
import FileUploader from './components/FileUploader'

export default function App() {
  const [context, setContext] = useState('')
  const [history, setHistory] = useState([])

  const handleSend = async (question) => {
    try {
      const response = await axios.post('/api/ask', { question, context })
      setHistory(prev => [...prev, { question, answer: response.data.answer }])
    } catch (error) {
      setHistory(prev => [...prev, { question, answer: '❌ Error: ' + error.response?.data?.error || error.message }])
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>LLM Document Analyzer</h2>
      <FileUploader onTextLoaded={setContext} />
      <ChatWindow onSend={handleSend} history={history} />
    </div>
  )
}
