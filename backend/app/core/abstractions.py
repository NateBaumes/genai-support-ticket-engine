from abc import ABC, abstractmethod
from typing import Dict, Any, List

class LLMProvider(ABC):
    @abstractmethod
    async def classify_ticket(self, text: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def generate_resolution(self, text: str, similar_tickets: List[Dict]) -> str:
        pass

class VectorStore(ABC):
    @abstractmethod
    async def upsert(self, id: str, vector: List[float], metadata: Dict):
        pass
    
    @abstractmethod
    async def query(self, vector: List[float], top_k: int = 5) -> List[Dict]:
        pass

class VendorClient(ABC):
    @abstractmethod
    async def send_notification(self, channel: str, message: str) -> bool:
        pass
