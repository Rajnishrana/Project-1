// frontend/src/components/FileUploader.jsx
import React from 'react'

export default function FileUploader({ onTextLoaded }) {
  const handleUpload = (e) => {
    const file = e.target.files[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = () => onTextLoaded(reader.result)
    reader.readAsText(file, 'utf-8')
  }

  return (
    <div>
      <textarea
        rows={6}
        style={{ width: '100%' }}
        placeholder="Paste text here..."
        onChange={(e) => onTextLoaded(e.target.value)}
      />
      <input type="file" accept=".txt" onChange={handleUpload} />
    </div>
  )
}
