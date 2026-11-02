from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app import models
from app.config.database import Base, SesionLocal, engine
from app.routers import auth_router, categoria_router, producto_router, usuario_router
from app.services import usuario_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SesionLocal() as db:
        usuario_service.crear_admin_inicial(db)
    yield


app = FastAPI(title="API de La Cosecha", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(usuario_router.router)
app.include_router(categoria_router.router)
app.include_router(producto_router.router)

@app.get("/")
def raiz():
    return {"mensaje": "API de La Cosecha en línea 🌾"}