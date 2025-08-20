import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
const API = import.meta.env.VITE_API_URL || ''

export default function Register(){
  const [email,setEmail]=useState('')
  const [password,setPassword]=useState('')
  const [full,setFull]=useState('')
  const nav = useNavigate()
  const [msg,setMsg]=useState('')

  async function submit(e){
    e.preventDefault(); setMsg('')
    try{
      await axios.post(`${API}/api/auth/register`, { email, password, full_name: full })
      setMsg('Registered! You can login now.')
      setTimeout(()=>nav('/login'), 1000)
    }catch(err){ setMsg(err?.response?.data?.detail || 'Register failed') }
  }

  return (
    <div style={{maxWidth:420, margin:'60px auto'}} className="card">
      <h2>Create account</h2>
      <form onSubmit={submit}>
        <div style={{marginBottom:8}}><input className="input" placeholder="Full name" value={full} onChange={e=>setFull(e.target.value)} /></div>
        <div style={{marginBottom:8}}><input className="input" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} /></div>
        <div style={{marginBottom:12}}><input className="input" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} /></div>
        <div><button className="btn" type="submit">Register</button></div>
      </form>
      {msg && <p style={{color:'lightgreen'}}>{msg}</p>}
    </div>
  )
}
