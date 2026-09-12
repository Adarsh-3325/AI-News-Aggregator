from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status, Depends
from app.database.repository import Repository, repository
from app.api.schemas import (
    UserCreateRequest,
    UserTopicsUpdateRequest,
    UserResponse,
    ScheduleSettings
)

router = APIRouter(prefix="/api/users", tags=["Users"])

def _format_user_response(user) -> UserResponse:
    user_topics = []
    if hasattr(user, "topics") and user.topics:
        for t in user.topics:
            user_topics.append({
                "name": t.topic_name,
                "scope": t.scope,
                "category": t.category
            })
    return UserResponse(
        email=user.email,
        is_subscribed=user.is_subscribed,
        topics=user_topics,
        schedule=ScheduleSettings(
            time=user.schedule_time or "23:00",
            frequency=user.schedule_freq or "daily",
            timezone=user.schedule_tz or "Asia/Kolkata",
            enabled=user.is_subscribed
        ),
        created_at=user.created_at
    )

@router.post("", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def create_or_get_user(payload: UserCreateRequest):
    """Creates a new user or returns existing user by email."""
    email = payload.email.lower().strip()
    user = repository.create_or_get_user(email=email, full_name=payload.full_name)
    return _format_user_response(user)

@router.get("/{email}", response_model=UserResponse)
async def get_user_profile(email: str):
    """Fetches user profile, selected topics, and schedule settings."""
    email_clean = email.lower().strip()
    user = repository.get_user_by_email(email_clean)
    if not user:
        # Auto-create if first visit
        user = repository.create_or_get_user(email_clean)
    return _format_user_response(user)

@router.put("/{email}/topics", response_model=UserResponse)
async def update_user_topics_put(email: str, payload: UserTopicsUpdateRequest):
    """Updates user's selected topics."""
    if not payload.topics:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one topic must be selected."
        )
    
    email_clean = email.lower().strip()
    topic_names = []
    for item in payload.topics:
        if isinstance(item, str):
            topic_names.append(item)
        elif isinstance(item, dict) and "name" in item:
            topic_names.append(item["name"])
        elif hasattr(item, "name"):
            topic_names.append(getattr(item, "name"))
            
    repository.update_user_topics(email=email_clean, topic_names=topic_names)
    user = repository.get_user_by_email(email_clean)
    return _format_user_response(user)

@router.post("/{email}/topics", response_model=UserResponse)
async def update_user_topics_post(email: str, payload: UserTopicsUpdateRequest):
    """POST endpoint for updating user topics (alias for PUT)."""
    return await update_user_topics_put(email, payload)

@router.delete("/{email}", status_code=status.HTTP_200_OK)
async def delete_user_account(email: str):
    """Permanently deletes user account and preferences."""
    email_clean = email.lower().strip()
    success = repository.delete_user(email_clean)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{email_clean}' not found."
        )
    
    return {
        "status": "success",
        "message": f"Account '{email_clean}' and all preferences have been deleted.",
        "email": email_clean
    }
