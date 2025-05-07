import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from agents.financial_data_agent import FinancialDataAgent, FinancialData
from pydantic import BaseModel
from utils.encryption import A2ASecurity

class ThreatAlert(BaseModel):
    threat_type: str
    details: dict

class ThreatDetectorAgent:
    def __init__(self, secret_key="your-strong-secret-key"):
        self.financial_agent = FinancialDataAgent()
        self.security = A2ASecurity(secret_key=secret_key)

    def analyze_workflow(self, data: dict, token: str) -> ThreatAlert:
        payload = self.security.verify_jwt_token(token)
        if not payload:
            return ThreatAlert(threat_type="Unauthorized", details={})

        financial_data = FinancialData(**data)
        result = self.financial_agent.detect_sensitive_data(financial_data)

        if result["credit_cards"] or result["is_anomalous"]:
            return ThreatAlert(
                threat_type="DataExfiltration",
                details=result
            )
        return ThreatAlert(threat_type="None", details={})

if __name__ == "__main__":
    agent = ThreatDetectorAgent()
    security = agent.security
    valid_token = security.create_jwt_token("agent1")
    invalid_token = "invalid_token"

    sample_data = {
        "text": "Card: 1234-5678-9012-3456",
        "transaction_amount": 15000
    }

    alert = agent.analyze_workflow(sample_data, valid_token)
    print("With valid token:", alert.model_dump_json(indent=2))

    alert_invalid = agent.analyze_workflow(sample_data, invalid_token)
    print("With invalid token:", alert_invalid.model_dump_json(indent=2))
