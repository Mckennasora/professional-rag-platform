from fastapi import FastAPI

from app.api.routes_chat import router as chat_router
from app.api.routes_document import router as document_router
from app.api.routes_eval import router as eval_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(chat_router, prefix="/api")
app.include_router(document_router, prefix="/api")
app.include_router(eval_router, prefix="/api")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
