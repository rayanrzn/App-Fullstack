import { Link } from 'react-router-dom'

const frameStyle = {
  maxWidth: '420px',
  margin: '40px auto',
  padding: '24px',
  border: '1px solid #ccc',
  borderRadius: '12px',
  background: '#fff',
  boxShadow: '0 6px 20px rgba(0,0,0,0.08)'
}

const sectionStyle = {
  marginBottom: '18px'
}

const navStyle = {
  display: 'flex',
  justifyContent: 'space-between',
  marginBottom: '20px'
}

function PageFrame({ title, description, children }) {
  return (
    <div style={frameStyle}>
      <div style={navStyle}>
        <Link to="/login">login</Link>
        <Link to="/register">inscription</Link>
        <Link to="/dashboard">dashboard</Link>
      </div>
      <h1 style={{ marginTop: 0 }}>{title}</h1>
      {description && <p style={{ marginTop: 0, marginBottom: '12px', color: '#555' }}>{description}</p>}
      <div style={sectionStyle}>{children}</div>
    </div>
  )
}

export default PageFrame
