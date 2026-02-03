import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import PageFrame from '../components/PageFrame'

function Chat() {
  const { token, logout } = useAuth()
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    if (!token) return
    fetchConversation()
  }, [token])

  const fetchConversation = async () => {
    try {
      const response = await fetch('http://localhost:8000/conversations', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      if (!response.ok) throw new Error('impossible de charger la conversation')
      const data = await response.json()
      setMessages(data.messages || [])
    } catch (err) {
      setError(err.message)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (!message.trim()) return

    const newMessages = [...messages, { role: 'user', content: message }]
    setMessages(newMessages)
    setMessage('')

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ message })
      })

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || 'erreur serveur')
      }

      const data = await response.json()
      setMessages((prev) => [...prev, { role: 'assistant', content: data.message }])
    } catch (err) {
      setError(err.message)
    }
  }

  if (!token) {
    return null
  }

  return (
    <PageFrame
      title="Neural Interface"
      description="Direct uplink to AI Core."
    >
      {error && <div style={{ color: 'var(--accent-error)' }}>{error}</div>}
      
      <div className="chat-container">
        {messages.length === 0 && <p style={{ textAlign: 'center', opacity: 0.5, marginTop: '20px' }}>System Ready. Awaiting Input.</p>}
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <strong>{msg.role === 'user' ? 'OPERATOR' : 'AI CORE'}</strong> 
            {msg.content}
          </div>
        ))}
      </div>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group" style={{ marginBottom: '16px' }}>
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type command..."
            autoFocus
          />
        </div>
        <button type="submit">
          Transmit
        </button>
      </form>
      
      <button onClick={logout} className="btn-danger" style={{ marginTop: '20px' }}>
        Terminate Session
      </button>
    </PageFrame>
  )
}

export default Chat
