import { Link, useLocation } from 'react-router-dom'

function PageFrame({ title, description, children }) {
  const location = useLocation()
  
  const isActive = (path) => location.pathname === path ? 'active' : ''

  return (
    <div className="glass-card">
      <div className="nav-container">
        <div className="nav-links">
          <Link to="/login" className={isActive('/login')}>Login</Link>
          <Link to="/register" className={isActive('/register')}>Join</Link>
        </div>
        <div className="nav-links">
          <Link to="/dashboard" className={isActive('/dashboard')}>Dashboard</Link>
        </div>
      </div>
      
      <h1>{title}</h1>
      {description && <p style={{ color: 'var(--text-secondary)', marginBottom: '24px', fontSize: '0.9rem' }}>{description}</p>}
      
      <div>{children}</div>
    </div>
  )
}

export default PageFrame
