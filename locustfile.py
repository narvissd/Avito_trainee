import random
import uuid

import requests
from locust import HttpUser, between, events, task

CREATED_USERS = []
CREATED_TEAMS = []
OPEN_PRS = []


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    base_url = environment.host

    for _ in range(5):
        team_name = f"team_{uuid.uuid4().hex[:6]}"
        members = []
        for _ in range(4):
            user_id = f"u_{uuid.uuid4().hex[:8]}"
            username = f"user_{uuid.uuid4().hex[:4]}"
            members.append({"user_id": user_id, "username": username, "is_active": True})
            CREATED_USERS.append(user_id)

        payload = {"team_name": team_name, "members": members}

        res = requests.post(f"{base_url}/team/add", json=payload)
        if res.status_code in [201, 400]:
            CREATED_TEAMS.append(team_name)


class PrServiceUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def create_pr(self):
        if not CREATED_USERS:
            return
        author_id = random.choice(CREATED_USERS)
        pr_id = f"pr-{uuid.uuid4().hex[:8]}"
        pr_name = f"TEST {uuid.uuid4().hex[:4]}"

        with self.client.post(
            "/pullRequest/create",
            json={"pull_request_id": pr_id, "pull_request_name": pr_name, "author_id": author_id},
            catch_response=True,
        ) as resp:
            if resp.status_code == 201:
                OPEN_PRS.append(pr_id)
            elif resp.status_code == 409:
                resp.success()

    @task(1)
    def merge_pr(self):
        if not OPEN_PRS:
            return
        pr_id = random.choice(OPEN_PRS)

        with self.client.post(
            "/pullRequest/merge", json={"pull_request_id": pr_id}, catch_response=True
        ) as resp:
            if resp.status_code == 200:
                if pr_id in OPEN_PRS:
                    OPEN_PRS.remove(pr_id)
            elif resp.status_code == 404:
                if pr_id in OPEN_PRS:
                    OPEN_PRS.remove(pr_id)
                resp.success()

    @task(2)
    def get_user_reviews(self):
        if not CREATED_USERS:
            return
        user_id = random.choice(CREATED_USERS)
        self.client.get(f"/users/getReview?user_id={user_id}", name="/users/getReview")

    @task(1)
    def get_team_info(self):
        if not CREATED_TEAMS:
            return
        team_name = random.choice(CREATED_TEAMS)
        self.client.get(f"/team/get?team_name={team_name}", name="/team/get")
