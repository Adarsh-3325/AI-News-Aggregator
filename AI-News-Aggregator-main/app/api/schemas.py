from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Literal, Any
from datetime import datetime

class TopicItem(BaseModel):
    name: str = Field(..., min_length=1, description="Topic name / query")
    scope: str = Field(default="general", description="Topic scope/type")
    category: Optional[str] = Field(default="general", description="Category tag")

    @classmethod
    def parse_item(cls, val: Any) -> "TopicItem":
        if isinstance(val, str):
            return cls(name=val, scope="general", category="general")
        if isinstance(val, dict):
            return cls(**val)
        return val

class ScheduleSettings(BaseModel):
    time: str = Field(default="23:00", description="Delivery time in HH:MM (24-hour format)")
    frequency: str = Field(default="daily", description="Delivery frequency")
    timezone: str = Field(default="Asia/Kolkata", description="IANA timezone name")
    enabled: bool = Field(default=True, description="Whether automated email digests are active")

class UserCreateRequest(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserTopicsUpdateRequest(BaseModel):
    topics: List[Any] = Field(..., description="List of selected topic strings or objects")

class UserResponse(BaseModel):
    email: str
    is_subscribed: bool = True
    topics: List[dict] = []
    schedule: ScheduleSettings = Field(default_factory=ScheduleSettings)
    created_at: Optional[datetime] = None

class AskQueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User query for LangGraph Agent")
    email: Optional[str] = None
    topics: Optional[List[str]] = None

class LiveSearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    topic: Optional[str] = None
    num_results: int = Field(default=6, ge=1, le=10)

class NewsPreviewRequest(BaseModel):
    topics: List[Any] = Field(default_factory=list)
