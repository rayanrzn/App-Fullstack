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
      title="dashboard"
      description="ta session est active, tu peux consulter les infos utilisateur et lancer le chatbot"
    >
      {user && (
        <div>
          <p>
            <strong>email:</strong> {user.email}
          </p>
          <p>
            <strong>id:</strong> {user.id}
          </p>
          <p>
            <strong>créé le:</strong> {user.created_at}
          </p>
        </div>
      )}
      <div style={{ marginTop: '16px' }}>
        <Link to="/chat" style={{ marginRight: '12px' }}>
          ouvrir le chatbot
        </Link>
        <button onClick={handleLogout}>se déconnecter</button>
      </div>
    </PageFrame>
  )
}

export default Dashboard
