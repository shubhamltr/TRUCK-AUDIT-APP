import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate, Link } from 'react-router-dom'

const API = import.meta.env.VITE_API_URL || ''

export default function Login(){
  const [email,setEmail]=useState('admin@example.com')
  const [password,setPassword]=useState('admin123')
  const [err,setErr]=useState('')
  const nav = useNavigate()

  async function submit(e){
    e.preventDefault(); setErr('')
    try{
      const params = new URLSearchParams()
      params.append('username', email)
      params.append('password', password)
      const res = await axios.post(`${API}/api/auth/login`, params, { headers: {'Content-Type':'application/x-www-form-urlencoded'} })
      localStorage.setItem('token', res.data.access_token)
      nav('/dashboard')
    }catch(err){ setErr(err?.response?.data?.detail || 'Login failed') }
  }

  return (
    <div style={{maxWidth:420, margin:'80px auto'}} className="card">
      <h2>Truck Audit — Login</h2>
      <form onSubmit={submit}>
        <div style={{marginBottom:8}}><input className="input" value={email} onChange={e=>setEmail(e.target.value)} /></div>
        <div style={{marginBottom:12}}><input type="password" className="input" value={password} onChange={e=>setPassword(e.target.value)} /></div>
        <div><button className="btn" type="submit">Login</button></div>
      </form>
      {err && <p style={{color:'salmon'}}>{err}</p>}
      <p style={{fontSize:12, opacity:.8}}>No account? <Link to="/register">Register</Link></p>
    </div>
  )
}
