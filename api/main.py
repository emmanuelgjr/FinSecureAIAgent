from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from utils.encryption import A2ASecurity
from agents.threat_detector_agent import ThreatDetectorAgent, ThreatAlert
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from simulations.attack_simulator import AttackSimulator

# Simulate attacks
# This is just for demonstration purposes and should not be used in production.
# In a real-world scenario, you would have a separate module for attack simulations.
# This module is used to simulate various attack scenarios for testing purposes.
# It should not be included in the production code.
# The AttackSimulator class is used to generate fake data for testing the threat detection system.
simulator = AttackSimulator()

# ✅ Add this line here:
SECRET_KEY = "super-secure-shared-key"

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ✅ Use the shared key here:
security = A2ASecurity(secret_key=SECRET_KEY)
threat_detector = ThreatDetectorAgent(secret_key=SECRET_KEY)


# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")

# Set up templates for HTML
templates = Jinja2Templates(directory="dashboard/templates")

# Pydantic input model
class FinancialDataInput(BaseModel):
    text: str
    transaction_amount: float

async def get_current_agent(token: str = Depends(oauth2_scheme)):
    payload = security.verify_jwt_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["agent_id"]

# API endpoint for analyzing financial data
@app.post("/analyze", response_model=ThreatAlert)
async def analyze_data(data: FinancialDataInput, agent_id: str = Depends(get_current_agent)):
    result = threat_detector.analyze_workflow(data.dict(), security.create_jwt_token(agent_id))
    return result

@app.get("/simulate/{attack_type}", response_model=ThreatAlert)
async def simulate_attack(attack_type: str, agent_id: str = Depends(get_current_agent)):
    if attack_type == "phishing":
        data = simulator.simulate_phishing()
    elif attack_type == "llm_leakage":
        data = simulator.simulate_llm_leakage()
    else:
        raise HTTPException(status_code=400, detail="Invalid attack type")

    return threat_detector.analyze_workflow(data, security.create_jwt_token(agent_id))

# Root endpoint serves dashboard
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
