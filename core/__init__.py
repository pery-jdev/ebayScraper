from fastapi import FastAPI 
from web.api.v1.routers import router as EbayAPIRouter
from web.app.routers import router as EbayAppRouter

def create_app() -> FastAPI:
    app: FastAPI = FastAPI()
    app.include_router(EbayAPIRouter)
    app.include_router(EbayAppRouter)
    return app