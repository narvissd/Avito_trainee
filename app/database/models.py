from sqlalchemy import Table, Column, String, Boolean, ForeignKey, DateTime, func, Enum
from app.database.db import metadata

pr_status_enum = Enum("OPEN", "MERGED", name="pr_status")

teams = Table(
    "teams",
    metadata,
    Column("name", String, primary_key=True),
)

users = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True),
    Column("username", String, nullable=False),
    Column("team_name", String, ForeignKey("teams.name"), nullable=False),
    Column("is_active", Boolean, default=True),
)

pull_requests = Table(
    "pull_requests",
    metadata,
    Column("id", String, primary_key=True),
    Column("name", String, nullable=False),
    Column("author_id", String, ForeignKey("users.id"), nullable=False),
    Column("status", pr_status_enum, default="OPEN"),
    Column("created_at", DateTime, server_default=func.now()),
    Column("merged_at", DateTime, nullable=True),
)

pr_reviewers = Table(
    "pr_reviewers",
    metadata,
    Column("pull_request_id", String, ForeignKey("pull_requests.id"), primary_key=True),
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
)