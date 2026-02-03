import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [user, setUser] = useState(null)

  // verifier si le token est valide au chargement
  useEffect(() => {
    if (token) {
      fetchUser()
    }
  }, [token])

  // recuperer les infos user
  const fetchUser = async () => {
    try {
      const response = await fetch('http://localhost:8000/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setUser(data)
      } else {
        // token invalide
        logout()
      }
    } catch (error) {
      console.error('Erreur:', error)
    }
  }

  // connecter l'utilisateur
  const login = async (email, password) => {
    const response = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    })

    if (response.ok) {
      const data = await response.json()
      localStorage.setItem('token', data.access_token)
      setToken(data.access_token)
      return { success: true }
    } else {
      const error = await response.json()
      return { success: false, error: error.detail }
    }
  }

  // inscrire un nouvel utilisateur
  const register = async (email, password) => {
    const response = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    })

    if (response.ok) {
      const data = await response.json()
      localStorage.setItem('token', data.access_token)
      setToken(data.access_token)
      return { success: true }
    } else {
      const error = await response.json()
      return { success: false, error: error.detail }
    }
  }

  // deconnecter l'utilisateur
  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
  }

  const isAuthenticated = !!token

  return (
    <AuthContext.Provider value={{ token, user, login, register, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
