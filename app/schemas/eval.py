from pydantic import BaseModel


class EvalStatusResponse(BaseModel):
    # TODO: Add evaluation job status and metrics summary.
    status: str
