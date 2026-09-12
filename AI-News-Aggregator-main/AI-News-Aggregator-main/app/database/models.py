from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer, Boolean, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    schedule_time: Mapped[str] = mapped_column(String(10), default="23:00")
    schedule_freq: Mapped[str] = mapped_column(String(20), default="daily")
    schedule_tz: Mapped[str] = mapped_column(String(50), default="Asia/Kolkata")
    is_subscribed: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    topics: Mapped[List["Topic"]] = relationship("Topic", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}')>"


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    topic_name: Mapped[str] = mapped_column(String(150), nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="general")
    query: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    scope: Mapped[str] = mapped_column(String(50), default="general")
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped[Optional["User"]] = relationship("User", back_populates="topics")

    def __repr__(self) -> str:
        return f"<Topic(id={self.id}, name='{self.topic_name}', category='{self.category}')>"


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), unique=True, nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g., "openai", "anthropic", "youtube", "google_news"
    category: Mapped[str] = mapped_column(String(100), default="general")
    topic_name: Mapped[str] = mapped_column(String(150), default="General News")
    raw_content: Mapped[str] = mapped_column(Text, nullable=False)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    scraped_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship to Digest (1-to-1)
    digest: Mapped[Optional["Digest"]] = relationship("Digest", back_populates="article", uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Article(id={self.id}, source='{self.source}', title='{self.title[:30]}...')>"


class Digest(Base):
    __tablename__ = "digests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), unique=True, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    key_takeaways: Mapped[str] = mapped_column(Text, nullable=False)  # JSON or newline-separated bullet points
    category: Mapped[str] = mapped_column(String(100), default="general")
    topic_name: Mapped[str] = mapped_column(String(150), default="General News")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    article: Mapped["Article"] = relationship("Article", back_populates="digest")
    sent_logs: Mapped[List["SentLog"]] = relationship("SentLog", back_populates="digest", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Digest(id={self.id}, article_id={self.article_id}, category='{self.category}')>"


class SentLog(Base):
    __tablename__ = "sent_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    digest_id: Mapped[int] = mapped_column(Integer, ForeignKey("digests.id", ondelete="CASCADE"), nullable=False, index=True)
    recipient: Mapped[str] = mapped_column(String(255), nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    digest: Mapped["Digest"] = relationship("Digest", back_populates="sent_logs")

    def __repr__(self) -> str:
        return f"<SentLog(id={self.id}, digest_id={self.digest_id}, recipient='{self.recipient}')>"


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    sources_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    from_live_search: Mapped[bool] = mapped_column(Boolean, default=False)
    grounded: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<AgentRun(id={self.id}, user_email='{self.user_email}', question='{self.question[:20]}...')>"

