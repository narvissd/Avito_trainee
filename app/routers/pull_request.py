from fastapi import APIRouter, HTTPException, status

from app.models.pull_request import PullRequests
from app.schemas.pull_request import PRCreate, PRMerge, PRReassign, PRReassignResponse, PRResponse

pr_router = APIRouter()


@pr_router.post(
    "/pullRequest/create", response_model=PRResponse, status_code=status.HTTP_201_CREATED
)
async def create_pr(body: PRCreate):
    result = await PullRequests.create(body.pull_request_id, body.pull_request_name, body.author_id)
    if result == "PR_EXISTS":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": {"code": "PR_EXISTS", "message": "PR id already exists"}},
        )

    if result == "AUTHOR_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "Author not found"}},
        )

    return {"pr": result}


@pr_router.post("/pullRequest/merge", response_model=PRResponse)
async def merge_pr(body: PRMerge):
    result = await PullRequests.merge(body.pull_request_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "PR not found"}},
        )

    return {"pr": result}


@pr_router.post("/pullRequest/reassign", response_model=PRReassignResponse)
async def reassign_reviewer(body: PRReassign):
    result = await PullRequests.reassign(body.pull_request_id, body.old_user_id)

    if result == "PR_NOT_FOUND":
        raise HTTPException(
            status_code=404, detail={"error": {"code": "NOT_FOUND", "message": "PR not found"}}
        )

    if result == "USER_NOT_FOUND":
        raise HTTPException(
            status_code=404, detail={"error": {"code": "NOT_FOUND", "message": "User not found"}}
        )

    if result == "PR_MERGED":
        raise HTTPException(
            status_code=409,
            detail={"error": {"code": "PR_MERGED", "message": "Cannot reassign on merged PR"}},
        )

    if result == "NOT_ASSIGNED":
        raise HTTPException(
            status_code=409,
            detail={
                "error": {"code": "NOT_ASSIGNED", "message": "Reviewer is not assigned to this PR"}
            },
        )

    if result == "NO_CANDIDATE":
        raise HTTPException(
            status_code=409,
            detail={
                "error": {
                    "code": "NO_CANDIDATE",
                    "message": "No active replacement candidate in team",
                }
            },
        )

    return result
