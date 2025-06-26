from fastapi import APIRouter
from app.models.strategy import StrategyRequest
from app.services.backtest import run_backtest

router = APIRouter(prefix="/strategy", tags=["Strategy"])

@router.post("/run")
async def run_strategy(request: StrategyRequest):
  return run_backtest(request)