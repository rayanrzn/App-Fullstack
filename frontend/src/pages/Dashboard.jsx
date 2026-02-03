import { useAuth } from '../context/AuthContext'
import { useNavigate, Link } from 'react-router-dom'
import PageFrame from '../components/PageFrame'

function Dashboard() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <PageFrame
      title="Identity Dashboard"
      description="Session Active. User Verification Complete."
    >
      {user && (
        <div style={{ marginBottom: '24px', background: 'rgba(0,0,0,0.3)', padding: '20px', borderRadius: '8px', border: '1px solid var(--glass-border)' }}>
          <div style={{ marginBottom: '12px' }}>
            <span style={{ display: 'block', fontSize: '0.7em', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>ID Code</span>
            <span style={{ fontFamily: 'Michroma', color: 'var(--accent-cyan)' }}>#{user.id}</span>
          </div>
          <div style={{ marginBottom: '12px' }}>
            <span style={{ display: 'block', fontSize: '0.7em', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>Protocol Email</span>
            <span style={{ fontSize: '1.1em' }}>{user.email}</span>
          </div>
          <div>
            <span style={{ display: 'block', fontSize: '0.7em', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>Inception Date</span>
            <span style={{ opacity: 0.8 }}>{new Date(user.created_at).toLocaleString()}</span>
          </div>
        </div>
      )}
      <div style={{ display: 'grid', gap: '16px' }}>
        <button onClick={() => navigate('/chat')}>
          Initialize Neural Link (Chat)
        </button>
        <button className="btn-danger" onClick={handleLogout}>
          Terminate Session
        </button>
      </div>
    </PageFrame>
  )
}

export default Dashboard
