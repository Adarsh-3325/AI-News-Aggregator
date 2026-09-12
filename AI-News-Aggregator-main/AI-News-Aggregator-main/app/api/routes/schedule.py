from fastapi import APIRouter, HTTPException, status
from app.database.repository import repository
from app.api.schemas import ScheduleSettings, UserResponse
from app.api.scheduler import schedule_user_job
from app.api.routes.users import _format_user_response

router = APIRouter(prefix="/api/users", tags=["Schedule"])

@router.put("/{email}/schedule", response_model=UserResponse)
async def update_user_schedule_put(email: str, payload: ScheduleSettings):
    """Updates user's delivery schedule settings and registers APScheduler job."""
    email_clean = email.lower().strip()
    user = repository.update_user_schedule(
        email=email_clean,
        schedule_time=payload.time,
        schedule_freq=payload.frequency,
        schedule_tz=payload.timezone,
        is_subscribed=payload.enabled
    )
    
    # Register/Reschedule APScheduler background job
    schedule_user_job(email_clean, payload)
    return _format_user_response(user)

@router.post("/{email}/schedule", response_model=UserResponse)
async def update_user_schedule_post(email: str, payload: ScheduleSettings):
    """POST alias for updating user's delivery schedule."""
    return await update_user_schedule_put(email, payload)

@router.post("/{email}/trigger")
async def trigger_user_digest_now(email: str, dry_run: bool = False):
    """Manually triggers the personalized digest pipeline for a user immediately."""
    email_clean = email.lower().strip()
    from app.services.pipeline_service import run_daily_pipeline
    success = run_daily_pipeline(dry_run=dry_run)
    return {"status": "completed" if success else "failed", "email": email_clean, "dry_run": dry_run}
