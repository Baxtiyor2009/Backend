from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        from models.models import create_tables
        await create_tables()
    except Exception as e:
        print(f"DB error: {e}")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.routes import auth, users, skins, orders, deposits, giveaways
from api.routes import admin, steam, payments, market, telegram

app.include_router(auth.router,      prefix="/api/auth")
app.include_router(users.router,     prefix="/api/users")
app.include_router(skins.router,     prefix="/api/skins")
app.include_router(orders.router,    prefix="/api/orders")
app.include_router(deposits.router,  prefix="/api/deposits")
app.include_router(giveaways.router, prefix="/api/giveaways")
app.include_router(admin.router,     prefix="/api/admin")
app.include_router(steam.router,     prefix="/api/steam")
app.include_router(payments.router,  prefix="/api/payments")
app.include_router(market.router,    prefix="/api/market")
app.include_router(telegram.router,  prefix="/api/telegram")

@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0.0"}

@app.get("/")
async def root():
    return {"name": "Blaze CS2 Marketplace"}
