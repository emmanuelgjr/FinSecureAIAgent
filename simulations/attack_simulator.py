from faker import Faker
import random

class AttackSimulator:
    def __init__(self):
        self.fake = Faker()

    def simulate_phishing(self) -> dict:
        """Simulate a phishing email containing fake credit card data."""
        return {
            "text": f"Dear user, your card {self.fake.credit_card_number()} needs verification.",
            "transaction_amount": random.uniform(50, 5000)
        }

    def simulate_llm_leakage(self) -> dict:
        """Simulate a data leakage scenario via a compromised LLM."""
        return {
            "text": f"LLM leak detected: Card - {self.fake.credit_card_number()}",
            "transaction_amount": random.uniform(500, 15000)
        }

if __name__ == "__main__":
    sim = AttackSimulator()
    print("Phishing Sample:", sim.simulate_phishing())
    print("LLM Leakage Sample:", sim.simulate_llm_leakage())
