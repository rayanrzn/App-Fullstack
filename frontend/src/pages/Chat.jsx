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
      title="chatbot"
      description="envoie un message, le bot répond et tu peux consulter l'historique"
    >
      {error && <p style={{ color: 'red', marginTop: 0 }}>{error}</p>}
      <div style={{ minHeight: '120px', background: '#f9f9f9', padding: '12px', borderRadius: '8px' }}>
        {messages.length === 0 && <p>aucun message pour le moment.</p>}
        {messages.map((msg, index) => (
          <p key={index} style={{ margin: '6px 0' }}>
            <strong>{msg.role}:</strong> {msg.content}
          </p>
        ))}
      </div>
      <form onSubmit={handleSubmit} style={{ marginTop: '12px' }}>
        <div>
          <label>message</label>
          <br />
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            style={{ width: '100%' }}
          />
        </div>
        <button type="submit" style={{ marginTop: '10px', width: '100%' }}>
          envoyer
        </button>
      </form>
      <button onClick={logout} style={{ marginTop: '16px' }}>
        quitter et se déconnecter
      </button>
    </PageFrame>
  )
}

export default Chat
