from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    from web.api.v1.routers import router as EbayAPIRouter
    from web.app.routers import router as EbayAppRouter
    
    app: FastAPI = FastAPI()

    app.include_router(EbayAPIRouter)
    app.include_router(EbayAppRouter)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Add your frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
