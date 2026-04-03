import React, { useState } from 'react'
import axios from 'axios'

function TicketForm({ onTicketCreated }) {
  const [formData, setFormData] = useState({
    customer_email: '',
    subject: '',
    description: ''
  })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      await axios.post('/api/tickets/create', formData)
      setFormData({ customer_email: '', subject: '', description: '' })
      onTicketCreated()
    } catch (error) {
      alert('Error: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Create Support Ticket</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Customer Email"
          value={formData.customer_email}
          onChange={(e) => setFormData({...formData, customer_email: e.target.value})}
          required
        />
        <input
          type="text"
          placeholder="Subject"
          value={formData.subject}
          onChange={(e) => setFormData({...formData, subject: e.target.value})}
          required
        />
        <textarea
          placeholder="Description"
          rows="4"
          value={formData.description}
          onChange={(e) => setFormData({...formData, description: e.target.value})}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Creating...' : 'Create Ticket'}
        </button>
      </form>
    </div>
  )
}

export default TicketForm
