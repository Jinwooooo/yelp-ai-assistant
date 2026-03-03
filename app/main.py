from fastapi import FastAPI
from app.core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title="Yelp AI Assistant",
        description="A production-grade RAG system mirroring Yelp's architecture.",
        version="1.0.0",
    )

    # Note: Routes will be registered here as we build them.
    # app.include_router(assistant_router)
    # app.include_router(content_router)

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app

app = create_app()
