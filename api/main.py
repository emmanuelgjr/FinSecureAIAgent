from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from utils.encryption import A2ASecurity
from agents.threat_detector_agent import ThreatDetectorAgent, ThreatAlert
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()

# Setup OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Security and agent initialization
security = A2ASecurity(secret_key="your-strong-secret-key")
threat_detector = ThreatDetectorAgent()

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

# Root endpoint serves dashboard
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
