# FinSecureAIAgent

FinSecureAIAgent is a multi-agent tool to detect and mitigate AI-driven financial data exfiltration, tailored specifically for American Express.

## Features

- Detection of sensitive financial data (Credit Card numbers, anomalous transactions)
- Agent-to-Agent (A2A) secured communication using JWT & AES encryption
- Financial threat simulations (phishing, LLM-driven data leakage)
- Web-based dashboard and API using FastAPI
- Integration with Azure Sentinel for logging and SOC automation
- Compliance with PCI DSS requirements

## Setup Guide

1. **Clone the repository**:
   ```bash
   git clone https://github.com/emmanuelgjr/FinSecureAIAgent.git
   cd FinSecureAIAgent

2. **Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8005

