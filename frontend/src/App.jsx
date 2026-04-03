import React, { useState } from 'react'
import TicketForm from './components/TicketForm'
import TicketList from './components/TicketList'
import toast, { Toaster } from 'react-hot-toast'

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0)
  const [selectedTicket, setSelectedTicket] = useState(null)

  const handleTicketCreated = () => {
    setRefreshTrigger(prev => prev + 1)
    toast.success('Ticket created! Processing...')
  }

  return (
    <div className="container">
      <Toaster position="top-right" />
      <h1>🤖 GenAI Support Ticket Engine</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <TicketForm onTicketCreated={handleTicketCreated} />
        <TicketList 
          refreshTrigger={refreshTrigger} 
          onSelectTicket={setSelectedTicket}
        />
      </div>
      
      {selectedTicket && (
        <div className="card">
          <h2>Ticket Details</h2>
          <pre style={{ whiteSpace: 'pre-wrap' }}>
            {JSON.stringify(selectedTicket, null, 2)}
          </pre>
          <button onClick={() => setSelectedTicket(null)}>Close</button>
        </div>
      )}
    </div>
  )
}

export default App
