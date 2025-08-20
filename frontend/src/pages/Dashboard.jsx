import React, { useEffect, useState } from 'react'
import axios from 'axios'

const API = import.meta.env.VITE_API_URL || ''

export default function Dashboard(){
  const [trucks,setTrucks]=useState([])
  const [reg,setReg]=useState('KA01AB1234')
  const [msg,setMsg]=useState('')
  const token = localStorage.getItem('token')

  useEffect(()=>{ if(!token) { window.location.href='/login'; return } 
    async function load(){ try{
      const res = await axios.get(`${API}/api/trucks/`, { headers: { Authorization: `Bearer ${token}` } })
      setTrucks(res.data)
    }catch(e){ setMsg('Unable to fetch - check API and token') } }
    load()
  },[])

  async function addTruck(e){
    e.preventDefault(); setMsg('')
    try{
      await axios.post(`${API}/api/trucks/`, { registration_number: reg }, { headers: { Authorization: `Bearer ${token}` } })
      setMsg('Truck added, reload to see it.')
    }catch(e){ setMsg('Add failed') }
  }

  return (
    <div style={{maxWidth:900, margin:'40px auto'}}>
      <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
        <h2>Dashboard</h2>
        <div>
          <button className="btn" onClick={()=>{ localStorage.removeItem('token'); window.location.href='/login' }}>Logout</button>
        </div>
      </div>
      <div className="card" style={{marginTop:12}}>
        <h3>Add Truck</h3>
        <form onSubmit={addTruck}><input className="input" value={reg} onChange={e=>setReg(e.target.value)} /><button className="btn" style={{marginLeft:8}}>Add</button></form>
        {msg && <p style={{color:'salmon'}}>{msg}</p>}
      </div>
      <div className="card" style={{marginTop:12}}>
        <h3>Your Trucks</h3>
        <ul>{trucks.map(t=> <li key={t.id}>{t.registration_number} — {t.capacity_mt ?? '—'} MT</li>)}</ul>
      </div>
    </div>
  )
}
