import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import PageFrame from '../components/PageFrame'

function Chat() {
  const { token } = useAuth()
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([])
  const [error, setError] = useState('')
  const [conversations, setConversations] = useState([])
  const [activeConvId, setActiveConvId] = useState(null)

  // 1. Charger la liste des conversations au démarrage
  useEffect(() => {
    if (token) fetchAllConversations()
  }, [token])

  // 2. Charger les messages quand on change de conversation
  useEffect(() => {
    if (activeConvId) fetchMessagesOfConversation(activeConvId)
  }, [activeConvId])

  const fetchAllConversations = async () => {
    try {
      const response = await fetch('http://localhost:8000/conversations', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const data = await response.json()
      setConversations(data)

      // Sélectionne la première discussion par défaut si elle existe
      if (data.length > 0 && !activeConvId) {
        setActiveConvId(data[0].id)
      }
    } catch (err) {
      setError("Erreur de chargement des discussions")
    }
  }

  const fetchMessagesOfConversation = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/conversations/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      const data = await response.json()
      // Le backend renvoie directement la liste [ {...}, {...} ]
      setMessages(Array.isArray(data) ? data : [])
    } catch (err) {
      setError("Erreur de chargement des messages")
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (!message.trim()) return

    let currentId = activeConvId

    // CRÉATION DE CONVERSATION SI BESOIN
    if (!currentId) {
      try {
        const res = await fetch('http://localhost:8000/conversations', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ titre: message.substring(0, 20) })
        });
        const newConv = await res.json();
        currentId = newConv.id;
        setActiveConvId(currentId);
        setConversations(prev => [...prev, newConv]);
      } catch (err) {
        setError("Impossible de créer la conversation");
        return;
      }
    }

    // MISE À JOUR LOCALE DE L'INTERFACE
    const userMsg = { role: 'user', content: message }
    setMessages(prev => [...prev, userMsg])
    const messageToSend = message // On stocke pour le body
    setMessage('')

    // ENVOI À L'IA
    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ 
          message: messageToSend, 
          conversation_id: currentId // Corrigé : minuscule
        })
      })

      if (!response.ok) {
        const errData = await response.json()
        throw new Error(errData.detail || 'Erreur serveur')
      }

      const data = await response.json()
      // Ajout de la réponse de l'IA
      setMessages(prev => [...prev, { role: 'assistant', content: data.message }])
    } catch (err) {
      setError(err.message)
    }
  }

  if (!token) return null

  return (
    <PageFrame title="Neural Interface" description="Direct uplink to AI Core.">
      <div style={{ display: 'flex', gap: '20px', minHeight: '500px' }}>

        {/* SIDEBAR */}
        <div className="sidebar" style={{ width: '200px', borderRight: '1px solid #444' }}>
          <h3 style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>UPLINKS</h3>
          {conversations.map(conv => (
            <div 
              key={conv.id} 
              onClick={() => setActiveConvId(conv.id)}
              style={{ 
                padding: '10px', 
                marginBottom: '5px',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '0.9rem',
                color: activeConvId === conv.id ? 'var(--accent-cyan)' : 'white',
                background: activeConvId === conv.id ? 'rgba(0,255,255,0.1)' : 'transparent',
                border: activeConvId === conv.id ? '1px solid var(--accent-cyan)' : '1px solid transparent'
              }}
            >
              {conv.titre || `Log_${conv.id}`}
            </div>
          ))}
          <button 
            onClick={() => { setActiveConvId(null); setMessages([]); }}
            style={{ width: '100%', marginTop: '10px', fontSize: '0.7rem' }}
          >
            + NEW LINK
          </button>
        </div>

        {/* CHAT AREA */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          {error && <div style={{ color: 'var(--accent-error)', padding: '10px', background: 'rgba(255,0,0,0.1)', borderRadius: '4px', marginBottom: '10px' }}>{error}</div>}
          
          <div className="chat-container" style={{ flex: 1, height: '400px', overflowY: 'auto', padding: '10px', background: 'rgba(0,0,0,0.2)', borderRadius: '8px' }}>
            {messages.length === 0 && <p style={{ textAlign: 'center', opacity: 0.5, marginTop: '150px' }}>Waiting for operator input...</p>}
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`} style={{ marginBottom: '15px' }}>
                <strong style={{ color: msg.role === 'user' ? 'var(--accent-cyan)' : 'var(--accent-purple)', fontSize: '0.8rem' }}>
                  {msg.role === 'user' ? '[OPERATOR]' : '[AI_CORE]'}:
                </strong> 
                <p style={{ margin: '5px 0 0 0', lineHeight: '1.4' }}>{msg.content}</p>
              </div>
            ))}
          </div>
          
          <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
            <input
              style={{ flex: 1 }}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Enter command lines..."
            />
            <button type="submit">TRANSMIT</button>
          </form>
        </div>
      </div>
    </PageFrame>
  )
}

export default Chat