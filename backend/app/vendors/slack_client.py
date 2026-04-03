import os
import httpx
from typing import Dict, Any
from app.core.abstractions import VendorClient

class SlackClient(VendorClient):
    def __init__(self):
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL", "")
        self.mock_mode = not self.webhook_url
    
    async def send_notification(self, channel: str, message: str) -> bool:
        if self.mock_mode:
            print(f"📧 [MOCK SLACK] {channel}: {message[:100]}...")
            return True
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.webhook_url, json={"text": message})
                return response.status_code == 200
        except Exception as e:
            print(f"❌ Slack failed: {e}")
            return False
    
    async def send_escalation(self, ticket: Dict[str, Any]) -> bool:
        message = f"""
🚨 *Ticket Escalation Required*
• ID: {ticket['ticket_id']}
• Customer: {ticket['customer']}
• Type: {ticket['type']}
• Sentiment: {ticket['sentiment']}
• Description: {ticket['description']}
        """
        return await self.send_notification("#support-escalations", message)
