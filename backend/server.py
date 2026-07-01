"""Bharat Climate Twin — FastAPI server."""
from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware
ROOT_DIR = Path(__file__).resolve().parent

env_file = ROOT_DIR / ".env"

print("========================================")
print("ROOT DIR :", ROOT_DIR)
print("ENV FILE :", env_file)
print("ENV EXISTS :", env_file.exists())

load_dotenv(dotenv_path=env_file, override=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("climate-twin")

mongo_url = os.getenv("MONGO_URL")
db_name = os.getenv("DB_NAME")

print("MONGO_URL =", mongo_url)
print("DB_NAME =", db_name)
print("========================================")

if not mongo_url:
    raise RuntimeError("MONGO_URL not found in .env")

if not db_name:
    raise RuntimeError("DB_NAME not found in .env")

client = AsyncIOMotorClient(mongo_url)
db = client[db_name] 








from services.auth_service import ensure_seed_users
from routes.auth import build_auth_router
from routes.climate import router as climate_router
from routes.monsoon import router as monsoon_router
from routes.extremes import router as extremes_router, drought_router
from routes.scenario import router as scenario_router, sector_router
from routes.advisor import build_advisor_router
from routes.geo import router as geo_router
from routes.saved import build_saved_router
from routes.export import router as export_router
from routes.grid import router as grid_router
from routes.lab import router as lab_router
from routes.farmer import router as farmer_router
from routes.policymaker import router as policymaker_router
from routes.districts import router as districts_router
from routes.hazards import router as hazards_router
from routes.bulletin import router as bulletin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await ensure_seed_users(db)
        logger.info("Seed users ensured.")
    except Exception as e:
        logger.warning(f"Seed users skipped: {e}")
    yield
    client.close()


app = FastAPI(title="Bharat Climate Twin API", version="1.0.0", lifespan=lifespan)

api = APIRouter(prefix="/api")


@api.get("/")
async def root():
    return {"service": "Bharat Climate Twin", "status": "online"}


@api.get("/health")
async def health():
    return {
        "status": "ok",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "timestamp_ist": datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=5, minutes=30))).isoformat(),
        "data_sources": {
            "nasa_power": "online",
            "open_meteo": "online",
            "era5_reanalysis": "online",
            "imd_style": "online",
        },
        "ai_model": "claude-sonnet-4-6 via Emergent Universal LLM key",
    }


# Mount sub-routers
api.include_router(build_auth_router(db))
api.include_router(climate_router)
api.include_router(monsoon_router)
api.include_router(extremes_router)
api.include_router(drought_router)
api.include_router(scenario_router)
api.include_router(sector_router)
api.include_router(build_advisor_router(db))
api.include_router(geo_router)
api.include_router(build_saved_router(db))
api.include_router(export_router)
api.include_router(grid_router)
api.include_router(lab_router)
api.include_router(farmer_router)
api.include_router(policymaker_router)
api.include_router(districts_router)
api.include_router(hazards_router)
api.include_router(bulletin_router)

app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)
