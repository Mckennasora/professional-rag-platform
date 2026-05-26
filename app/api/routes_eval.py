from fastapi import APIRouter

router = APIRouter(prefix="/eval", tags=["eval"])


@router.get("/status")
def eval_status() -> dict[str, str]:
    # TODO: Implement RAGAS and custom evaluation status endpoints.
    return {"status": "not implemented"}
