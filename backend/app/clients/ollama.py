import httpx
from app.config import settings
from app.utils.logging import get_logger
from typing import Optional

logger = get_logger(__name__)

class OllamaClient:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.available = self.base_url is not None
    
    async def generate_explanation(
        self,
        amount: float,
        incident_type: str,
        history_score: float,
        risk_score: float,
        fraud_probability: float
    ) -> Optional[str]:
        """Generate explanation using Ollama LLM."""
        if not self.available:
            return None
        
        risk_level = "LOW" if fraud_probability < 0.35 else "MEDIUM" if fraud_probability < 0.70 else "HIGH"
        
        prompt = f"""Explain why this insurance claim is considered {risk_level} risk based on these factors:
- Amount: ${amount:,.2f}
- Incident type: {incident_type}
- Customer history score: {history_score:.1f}/100
- Risk score: {risk_score:.2f}/100
- Fraud probability: {fraud_probability:.1%}

Provide 3 bullet reasons and 1 recommended next action. Keep it business-friendly and compliance-aware. Use professional insurance terminology."""
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", "").strip()
                else:
                    logger.warning(f"Ollama returned status {response.status_code}")
                    return None
        
        except Exception as e:
            logger.warning(f"Ollama request failed: {e}")
            return None

ollama_client = OllamaClient()
