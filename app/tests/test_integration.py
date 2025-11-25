import pytest


@pytest.mark.asyncio
async def test_full(client):
    team_payload = {
        "team_name": "test",
        "members": [
            {"user_id": "u1", "username": "alice", "is_active": True},
            {"user_id": "u2", "username": "bob", "is_active": True},
            {"user_id": "u3", "username": "charlie", "is_active": True},
            {"user_id": "u4", "username": "dave", "is_active": True},
        ],
    }
    resp = await client.post("/team/add", json=team_payload)
    assert resp.status_code == 201

    pr_payload = {"pull_request_id": "pr-100", "pull_request_name": "Feature", "author_id": "u1"}
    resp = await client.post("/pullRequest/create", json=pr_payload)
    assert resp.status_code == 201
    current_reviewers = resp.json()["pr"]["assigned_reviewers"]

    resp = await client.post(
        "/pullRequest/reassign", json={"pull_request_id": "pr-100", "old_user_id": "u1"}
    )
    assert resp.status_code == 409
    assert resp.json()["detail"]["error"]["code"] == "NOT_ASSIGNED"

    await client.post("/users/setIsActive", json={"user_id": "u4", "is_active": False})

    reviewer_to_replace = current_reviewers[0]
    resp = await client.post(
        "/pullRequest/reassign",
        json={"pull_request_id": "pr-100", "old_user_id": reviewer_to_replace},
    )

    if resp.status_code == 200:
        current_reviewers = resp.json()["pr"]["assigned_reviewers"]
    elif resp.status_code == 409:
        assert resp.json()["detail"]["error"]["code"] == "NO_CANDIDATE"

    await client.post("/users/setIsActive", json={"user_id": "u4", "is_active": True})

    reviewer_to_replace_round_2 = current_reviewers[0]

    resp = await client.post(
        "/pullRequest/reassign",
        json={"pull_request_id": "pr-100", "old_user_id": reviewer_to_replace_round_2},
    )
    assert resp.status_code == 200
    new_reviewer = resp.json()["replaced_by"]
    assert new_reviewer in resp.json()["pr"]["assigned_reviewers"]

    resp = await client.get("/users/getReview", params={"user_id": new_reviewer})
    assert resp.status_code == 200
    assert len(resp.json()["pull_requests"]) > 0

    resp = await client.post("/pullRequest/merge", json={"pull_request_id": "pr-100"})
    assert resp.status_code == 200
    assert resp.json()["pr"]["status"] == "MERGED"

    final_reviewer = resp.json()["pr"]["assigned_reviewers"][0]
    resp = await client.post(
        "/pullRequest/reassign", json={"pull_request_id": "pr-100", "old_user_id": final_reviewer}
    )
    assert resp.status_code == 409
    assert resp.json()["detail"]["error"]["code"] == "PR_MERGED"

    resp = await client.get("/stats")
    assert resp.status_code == 200
    assert resp.json()["pull_requests_merged"] == 1


@pytest.mark.asyncio
async def test_error(client):
    await client.post(
        "/team/add",
        json={
            "team_name": "Devs",
            "members": [{"user_id": "dev1", "username": "d1", "is_active": True}],
        },
    )

    resp = await client.post("/users/setIsActive", json={"user_id": "ghost", "is_active": False})
    assert resp.status_code == 404

    await client.post(
        "/pullRequest/create",
        json={"pull_request_id": "pr-1", "pull_request_name": "A", "author_id": "dev1"},
    )
    resp = await client.post(
        "/pullRequest/create",
        json={"pull_request_id": "pr-1", "pull_request_name": "B", "author_id": "dev1"},
    )
    assert resp.status_code == 409

    resp = await client.post(
        "/pullRequest/create",
        json={"pull_request_id": "pr-2", "pull_request_name": "C", "author_id": "unknown"},
    )
    assert resp.status_code == 404

    resp = await client.post("/pullRequest/merge", json={"pull_request_id": "pr-999"})
    assert resp.status_code == 404

    resp = await client.post(
        "/pullRequest/reassign", json={"pull_request_id": "pr-999", "old_user_id": "dev1"}
    )
    assert resp.status_code == 404

    resp = await client.get("/team/get", params={"team_name": "MissingTeam"})
    assert resp.status_code == 404

    resp = await client.post("/team/add", json={"team_name": "Devs", "members": []})
    assert resp.status_code == 400
