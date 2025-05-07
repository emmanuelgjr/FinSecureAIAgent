import re
from pydantic import BaseModel

class FinancialData(BaseModel):
    text: str
    transaction_amount: float = None

class FinancialDataAgent:
    def __init__(self):
        self.cc_pattern = r"\b(?:\d[ -]*?){13,16}\b"  # Simple regex for credit cards

    def detect_sensitive_data(self, data: FinancialData) -> dict:
        """Detect credit cards and transaction anomalies."""
        matches = re.findall(self.cc_pattern, data.text)
        is_anomalous = self._check_anomaly(data.transaction_amount)
        return {
            "credit_cards": matches,
            "is_anomalous": is_anomalous
        }

    def _check_anomaly(self, amount: float) -> bool:
        """Detect transactions over $10,000 as anomalies."""
        if amount is None:
            return False
        return amount > 10000

if __name__ == "__main__":
    agent = FinancialDataAgent()
    data = FinancialData(text="Card: 1234-5678-9012-3456", transaction_amount=15000)
    result = agent.detect_sensitive_data(data)
    print(result)
