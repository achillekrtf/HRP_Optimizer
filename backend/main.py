from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import database
import logic
import threading
import scheduler

app = FastAPI(title="HRP Portfolio API")

# Warning: Ideally, we shouldn't run the scheduler inside the same process worker 
# if we have multiple workers. But for a simple VPS setup with 1 worker, this is fine.
# Or we run scheduler.py separately in Docker. 
# Let's keep scheduler.py separate in Docker to be robust. 
# This API is just for serving data.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, tighten for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MetricResponse(BaseModel):
    expected_return: float
    volatility: float
    sharpe_ratio: float

class AllocationResponse(BaseModel):
    date: str
    weights: Dict[str, float]
    metrics: MetricResponse

@app.get("/")
def read_root():
    return {"status": "ok", "service": "HRP Optimizer API"}

@app.get("/allocation", response_model=AllocationResponse)
def get_allocation():
    data = database.get_latest_allocation()
    if not data:
        raise HTTPException(status_code=404, detail="No allocation found")
    return data

@app.get("/history")
def get_history_performance():
    # Helper to return simple cumulative performance series
    # Reuse logic from logic.py or just fetch prices
    # For MVP, let's just return the prices so Frontend can calculate/chart it
    # Or return the pre-calculated series
    
    # Let's return raw normalized prices for Top 7 + SPY
    df = database.get_prices()
    if df.empty:
        return {"data": []}
    
    # Normalize to 100
    df_norm = (df / df.iloc[0]) * 100
    
    # Convert to JSON friendly format (list of dicts with date)
    reset = df_norm.reset_index()
    reset['date'] = reset['date'].dt.strftime('%Y-%m-%d')
    return reset.to_dict(orient="records")

@app.post("/rebalance")
def trigger_rebalance():
    """Manual trigger"""
    logic.update_market_data()
    logic.rebalance_portfolio_if_needed()
    return {"status": "triggered"}
