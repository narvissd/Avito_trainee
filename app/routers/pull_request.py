from fastapi import APIRouter, HTTPException, status
from app.schemas.pull_request import PRCreate, PRResponse, PRMerge
from app.models.pull_request import PullRequests

pr_router = APIRouter()


@pr_router.post("/pullRequest/create", response_model=PRResponse, status_code=status.HTTP_201_CREATED)
async def create_pr(body: PRCreate):
    result = await PullRequests.create(
        body.pull_request_id,
        body.pull_request_name,
        body.author_id
    )
    if result == "PR_EXISTS":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": {"code": "PR_EXISTS", "message": "PR id already exists"}}
        )

    if result == "AUTHOR_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "Author not found"}}
        )

    return {"pr": result}


@pr_router.post("/pullRequest/merge", response_model=PRResponse)
async def merge_pr(body: PRMerge):
    result = await PullRequests.merge(body.pull_request_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "PR not found"}}
        )

    return {"pr": result}
