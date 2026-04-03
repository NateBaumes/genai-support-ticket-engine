import React, { useState, useEffect } from 'react'
import axios from 'axios'

function TicketList({ refreshTrigger, onSelectTicket }) {
  const [tickets, setTickets] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTickets()
  }, [refreshTrigger])

  const fetchTickets = async () => {
    try {
      const response = await axios.get('/api/tickets/')
      setTickets(response.data)
    } catch (error) {
      console.error('Failed to fetch tickets:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusClass = (status) => {
    if (!status) return ''
    switch(status) {
      case 'pending': return 'status-pending'
      case 'processed': return 'status-processed'
      case 'escalated': return 'status-escalated'
      default: return ''
    }
  }

  if (loading) return <div className="card">Loading tickets...</div>

  return (
    <div className="card">
      <h2>Recent Tickets</h2>
      {tickets.length === 0 ? (
        <p>No tickets yet. Create one!</p>
      ) : (
        tickets.map(ticket => (
          <div 
            key={ticket.id} 
            className="ticket-item"
            onClick={() => onSelectTicket(ticket)}
          >
            <div style={{ fontWeight: 'bold' }}>{ticket.id}</div>
            <div style={{ fontSize: '14px', color: '#666' }}>{ticket.subject}</div>
            <div style={{ fontSize: '12px', marginTop: '4px' }}>
              <span className={getStatusClass(ticket.status)}>
                {ticket.status || 'unknown'}
              </span>
              {ticket.sentiment && (
                <span style={{ marginLeft: '8px' }}>🎭 {ticket.sentiment}</span>
              )}
            </div>
          </div>
        ))
      )}
    </div>
  )
}

export default TicketList
