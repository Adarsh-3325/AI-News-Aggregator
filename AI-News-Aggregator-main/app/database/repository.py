import json
import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, delete

from app.database.models import User, Topic, Article, Digest, SentLog, AgentRun
from app.database.connection import SessionLocal, init_db
from app.database.chroma import chroma_store, ChromaVectorStore

logger = logging.getLogger(__name__)

# Default topic configuration for seeding
DEFAULT_TOPICS = [
    {
        "topic_name": "Frontier AI & LLMs",
        "category": "ai",
        "scope": "ai",
        "query": "Artificial Intelligence LLM OpenAI Anthropic DeepSeek",
        "location": "",
        "weight": 1.5,
        "active": True
    },
    {
        "topic_name": "Local Ghaziabad News",
        "category": "local",
        "scope": "local",
        "query": "Ghaziabad news development municipal UP",
        "location": "Ghaziabad, India",
        "weight": 1.2,
        "active": True
    },
    {
        "topic_name": "National News & Politics",
        "category": "politics",
        "scope": "national",
        "query": "India politics economy policy government",
        "location": "India",
        "weight": 1.0,
        "active": True
    },
    {
        "topic_name": "Global Geopolitics",
        "category": "international",
        "scope": "international",
        "query": "world politics diplomacy global economy",
        "location": "",
        "weight": 1.0,
        "active": True
    },
    {
        "topic_name": "Cricket & Sports",
        "category": "sports",
        "scope": "sports",
        "query": "cricket match India tournament sports",
        "location": "India",
        "weight": 0.9,
        "active": True
    },
    {
        "topic_name": "Delhi NCR Weather",
        "category": "weather",
        "scope": "weather",
        "query": "Delhi NCR weather forecast temperature",
        "location": "Delhi, India",
        "weight": 1.0,
        "active": True
    }
]

class Repository:
    """
    Unified Data Access Layer:
    - PostgreSQL / SQLite via SQLAlchemy for relational tables
    - ChromaDB for vector similarity search and article embeddings
    """

    def __init__(self, session: Optional[Session] = None, vector_store: Optional[ChromaVectorStore] = None):
        self._session = session
        self.vector_store = vector_store or chroma_store

    def _get_session(self) -> Session:
        if self._session:
            return self._session
        return SessionLocal()

    # ==================== USER & TOPIC METHODS ====================

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Finds user record by email with eagerly loaded topics."""
        clean_email = email.strip().lower()
        db = self._get_session()
        try:
            return db.scalar(select(User).options(selectinload(User.topics)).where(User.email == clean_email))
        finally:
            if not self._session:
                db.close()

    def create_or_get_user(self, email: str, full_name: Optional[str] = None) -> User:
        """Creates user with default topics if not existing."""
        clean_email = email.strip().lower()
        db = self._get_session()
        try:
            user = db.scalar(select(User).options(selectinload(User.topics)).where(User.email == clean_email))
            if not user:
                user = User(
                    email=clean_email,
                    full_name=full_name or clean_email.split("@")[0]
                )
                db.add(user)
                db.commit()

                # Seed default user topics
                for t in DEFAULT_TOPICS:
                    topic = Topic(
                        user_id=user.id,
                        topic_name=t["topic_name"],
                        category=t["category"],
                        query=t["query"],
                        location=t["location"],
                        scope=t["scope"],
                        weight=t["weight"],
                        active=True
                    )
                    db.add(topic)
                db.commit()
                # Re-query with selectinload to ensure topics are attached and loaded
                user = db.scalar(select(User).options(selectinload(User.topics)).where(User.email == clean_email))
            return user
        finally:
            if not self._session:
                db.close()


    def update_user_topics(self, email: str, topic_names: List[str]) -> List[Topic]:
        """Replaces user topics with selected topic names."""
        clean_email = email.strip().lower()
        db = self._get_session()
        try:
            user = db.scalar(select(User).where(User.email == clean_email))
            if not user:
                user = User(email=clean_email, full_name=clean_email.split("@")[0])
                db.add(user)
                db.commit()

            # Delete old topics
            db.execute(delete(Topic).where(Topic.user_id == user.id))
            db.commit()

            # Map matching default topics or custom topics
            updated_topics = []
            default_map = {t["topic_name"]: t for t in DEFAULT_TOPICS}

            for name in topic_names:
                t_info = default_map.get(name, {
                    "category": "custom",
                    "scope": "custom",
                    "query": name,
                    "location": "",
                    "weight": 1.0
                })
                topic = Topic(
                    user_id=user.id,
                    topic_name=name,
                    category=t_info["category"],
                    query=t_info.get("query", name),
                    location=t_info.get("location", ""),
                    scope=t_info.get("scope", "custom"),
                    weight=t_info.get("weight", 1.0),
                    active=True
                )
                db.add(topic)
                updated_topics.append(topic)

            db.commit()
            return updated_topics
        finally:
            if not self._session:
                db.close()

    def update_user_schedule(
        self,
        email: str,
        schedule_time: str = "23:00",
        schedule_freq: str = "daily",
        schedule_tz: str = "Asia/Kolkata",
        is_subscribed: bool = True
    ) -> User:
        """Updates delivery schedule for a user."""
        clean_email = email.strip().lower()
        db = self._get_session()
        try:
            user = db.scalar(select(User).options(selectinload(User.topics)).where(User.email == clean_email))
            if not user:
                user = User(email=clean_email, full_name=clean_email.split("@")[0])
                db.add(user)
                db.commit()

            user.schedule_time = schedule_time
            user.schedule_freq = schedule_freq
            user.schedule_tz = schedule_tz
            user.is_subscribed = is_subscribed
            db.commit()

            user = db.scalar(select(User).options(selectinload(User.topics)).where(User.email == clean_email))
            return user
        finally:
            if not self._session:
                db.close()


    def delete_user(self, email: str) -> bool:
        """Deletes user and associated settings."""
        clean_email = email.strip().lower()
        db = self._get_session()
        try:
            user = db.scalar(select(User).where(User.email == clean_email))
            if user:
                db.delete(user)
                db.commit()
                return True
            return False
        finally:
            if not self._session:
                db.close()

    def get_active_topics(self) -> List[Dict[str, Any]]:
        """Returns all global active topic definitions."""
        db = self._get_session()
        try:
            topics = list(db.scalars(select(Topic).where(Topic.active == True)).all())
            if not topics:
                return DEFAULT_TOPICS
            return [
                {
                    "topic_name": t.topic_name,
                    "category": t.category,
                    "query": t.query,
                    "location": t.location,
                    "scope": t.scope,
                    "weight": t.weight,
                    "active": t.active
                }
                for t in topics
            ]
        finally:
            if not self._session:
                db.close()

    # ==================== ARTICLE METHODS ====================

    def save_article(
        self,
        title: str,
        url: str,
        source: str,
        raw_content: str,
        category: str = "general",
        topic_name: str = "General News",
        published_at: Optional[datetime] = None
    ) -> Optional[Article]:
        """Idempotently saves article if URL does not already exist."""
        db = self._get_session()
        try:
            existing = db.scalar(select(Article).where(Article.url == url))
            if existing:
                return None  # Skip duplicate URL

            article = Article(
                title=title,
                url=url,
                source=source,
                category=category,
                topic_name=topic_name,
                raw_content=raw_content,
                published_at=published_at or datetime.now(timezone.utc)
            )
            db.add(article)
            db.commit()
            db.refresh(article)
            return article
        finally:
            if not self._session:
                db.close()

    def get_unprocessed_articles(self) -> List[Article]:
        """Returns articles that do not have an LLM summary digest yet."""
        db = self._get_session()
        try:
            stmt = select(Article).outerjoin(Digest).where(Digest.id.is_(None))
            return list(db.scalars(stmt).all())
        finally:
            if not self._session:
                db.close()

    # ==================== DIGEST METHODS ====================

    def save_digest(
        self,
        article_id: int,
        summary: str,
        key_takeaways: str,
        category: str = "general",
        topic_name: str = "General News"
    ) -> Digest:
        """Saves LLM digest document for an article."""
        db = self._get_session()
        try:
            digest = Digest(
                article_id=article_id,
                summary=summary,
                key_takeaways=key_takeaways,
                category=category,
                topic_name=topic_name
            )
            db.add(digest)
            db.commit()
            db.refresh(digest)
            return digest
        finally:
            if not self._session:
                db.close()

    def get_unsent_digests(self) -> List[Dict[str, Any]]:
        """Returns digests and associated articles that have not been emailed."""
        db = self._get_session()
        try:
            stmt = select(Digest, Article).join(Article, Digest.article_id == Article.id).outerjoin(SentLog).where(SentLog.id.is_(None))
            results = db.execute(stmt).all()
            output = []
            for d, a in results:
                output.append({
                    "_id": d.id,
                    "id": d.id,
                    "article_id": a.id,
                    "summary": d.summary,
                    "key_takeaways": d.key_takeaways,
                    "category": d.category,
                    "topic_name": d.topic_name,
                    "created_at": d.created_at,
                    "article": {
                        "_id": a.id,
                        "title": a.title,
                        "url": a.url,
                        "source": a.source,
                        "raw_content": a.raw_content,
                        "published_at": a.published_at
                    }
                })
            return output
        finally:
            if not self._session:
                db.close()

    # ==================== SENT LOG METHODS ====================

    def log_sent_digest(self, digest_id: int, recipient: str) -> SentLog:
        """Records delivered digest to prevent duplicate emails."""
        db = self._get_session()
        try:
            log_entry = SentLog(digest_id=digest_id, recipient=recipient)
            db.add(log_entry)
            db.commit()
            db.refresh(log_entry)
            return log_entry
        finally:
            if not self._session:
                db.close()

    # ==================== AGENT LOG METHODS ====================

    def log_agent_run(
        self,
        user_email: Optional[str],
        question: str,
        answer: str,
        sources: List[Dict[str, Any]],
        from_live_search: bool,
        grounded: bool
    ) -> AgentRun:
        """Records agent RAG execution for monitoring and metrics."""
        db = self._get_session()
        try:
            run = AgentRun(
                user_email=user_email,
                question=question,
                answer=answer,
                sources_json=json.dumps(sources),
                from_live_search=from_live_search,
                grounded=grounded
            )
            db.add(run)
            db.commit()
            db.refresh(run)
            return run
        finally:
            if not self._session:
                db.close()

    # ==================== VECTOR EMBEDDING (CHROMADB) METHODS ====================

    def save_article_embedding(
        self,
        article_id: Any,
        digest_id: Any,
        topic: str,
        title: str,
        text: str,
        embedding: List[float],
        source_url: str = "",
        published_at: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Saves embedding into ChromaDB vector store."""
        return self.vector_store.save_article_embedding(
            article_id=article_id,
            digest_id=digest_id,
            topic=topic,
            title=title,
            text=text,
            embedding=embedding,
            source_url=source_url,
            published_at=published_at
        )

    def get_unembedded_digests(self) -> List[Dict[str, Any]]:
        """Returns digests in SQL database that are not yet stored in ChromaDB."""
        existing_ids = self.vector_store.get_existing_digest_ids()
        db = self._get_session()
        try:
            stmt = select(Digest, Article).join(Article, Digest.article_id == Article.id)
            results = db.execute(stmt).all()
            unembedded = []
            for d, a in results:
                if str(d.id) not in existing_ids:
                    unembedded.append({
                        "_id": d.id,
                        "id": d.id,
                        "article_id": a.id,
                        "summary": d.summary,
                        "key_takeaways": d.key_takeaways,
                        "category": d.category,
                        "topic_name": d.topic_name,
                        "article": {
                            "_id": a.id,
                            "title": a.title,
                            "url": a.url,
                            "source": a.source,
                            "raw_content": a.raw_content,
                            "published_at": a.published_at
                        }
                    })
            return unembedded
        finally:
            if not self._session:
                db.close()

    def vector_search(
        self,
        query_vector: List[float],
        limit: int = 6,
        topics: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Executes vector similarity search against ChromaDB."""
        return self.vector_store.vector_search(
            query_vector=query_vector,
            limit=limit,
            topics=topics
        )

# Instantiate global repository instance
repository = Repository()
MongoRepository = Repository  # Backward compatibility alias
