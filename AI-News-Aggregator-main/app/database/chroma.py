import os
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings

logger = logging.getLogger(__name__)

class ChromaVectorStore:
    _instance: Optional["ChromaVectorStore"] = None

    def __new__(cls) -> "ChromaVectorStore":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_chroma()
        return cls._instance

    def _init_chroma(self) -> None:
        """Initializes persistent ChromaDB client and collection."""
        persist_dir = settings.CHROMA_PERSIST_DIR
        os.makedirs(persist_dir, exist_ok=True)

        try:
            self.client = chromadb.PersistentClient(path=persist_dir)
            self.collection = self.client.get_or_create_collection(
                name="article_embeddings",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"[ChromaDB] Persistent collection initialized at '{persist_dir}'.")
        except Exception as e:
            logger.error(f"[ChromaDB ERROR] Failed to initialize persistent ChromaDB client: {e}")
            raise e

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
        """Upserts an article vector embedding document into ChromaDB."""
        doc_id = f"digest_{digest_id}"
        pub_str = published_at.isoformat() if isinstance(published_at, datetime) else str(published_at or "")

        metadata = {
            "article_id": int(article_id) if str(article_id).isdigit() else str(article_id),
            "digest_id": int(digest_id) if str(digest_id).isdigit() else str(digest_id),
            "topic": topic or "General News",
            "title": title or "Untitled Article",
            "source_url": source_url or "",
            "published_at": pub_str,
        }

        try:
            self.collection.upsert(
                ids=[doc_id],
                embeddings=[embedding],
                metadatas=[metadata],
                documents=[text]
            )
            logger.info(f"[ChromaDB] Saved embedding for document '{doc_id}' ({title[:30]}).")
        except Exception as e:
            logger.error(f"[ChromaDB ERROR] Failed to upsert vector document {doc_id}: {e}")

        return {
            "id": doc_id,
            "metadata": metadata,
            "text": text
        }

    def vector_search(
        self,
        query_vector: List[float],
        limit: int = 6,
        topics: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes vector similarity search in ChromaDB.
        Optionally filters by topic if topics filter is provided.
        """
        if self.collection.count() == 0:
            logger.warning("[ChromaDB] Collection is currently empty.")
            return []

        where_clause = None
        if topics and len(topics) > 0:
            if len(topics) == 1:
                where_clause = {"topic": topics[0]}
            else:
                where_clause = {"$or": [{"topic": t} for t in topics]}

        try:
            results = self.collection.query(
                query_embeddings=[query_vector],
                n_results=min(limit, self.collection.count()),
                where=where_clause,
                include=["documents", "metadatas", "distances"]
            )
        except Exception as e:
            logger.error(f"[ChromaDB ERROR] Vector search with filter failed: {e}. Trying without topic filter...")
            results = self.collection.query(
                query_embeddings=[query_vector],
                n_results=min(limit, self.collection.count()),
                include=["documents", "metadatas", "distances"]
            )

        output: List[Dict[str, Any]] = []
        if results and results.get("ids") and len(results["ids"]) > 0:
            ids = results["ids"][0]
            documents = results["documents"][0] if results.get("documents") else []
            metadatas = results["metadatas"][0] if results.get("metadatas") else []
            distances = results["distances"][0] if results.get("distances") else []

            for idx in range(len(ids)):
                meta = metadatas[idx] if idx < len(metadatas) else {}
                doc_text = documents[idx] if idx < len(documents) else ""
                dist = distances[idx] if idx < len(distances) else 1.0

                # Cosine distance to similarity score: similarity = 1 - distance
                score = round(max(0.0, 1.0 - float(dist)), 4)

                pub_date_raw = meta.get("published_at")
                pub_date = None
                if pub_date_raw:
                    try:
                        pub_date = datetime.fromisoformat(pub_date_raw)
                    except Exception:
                        pub_date = None

                output.append({
                    "id": ids[idx],
                    "article_id": meta.get("article_id"),
                    "digest_id": meta.get("digest_id"),
                    "topic": meta.get("topic", "General"),
                    "title": meta.get("title", "Untitled"),
                    "text": doc_text,
                    "source_url": meta.get("source_url", ""),
                    "published_at": pub_date,
                    "score": score
                })

        # Sort by similarity score descending
        output.sort(key=lambda x: x.get("score", 0.0), reverse=True)
        return output

    def get_existing_digest_ids(self) -> set:
        """Returns set of integer or string digest IDs already present in ChromaDB."""
        if self.collection.count() == 0:
            return set()

        all_records = self.collection.get(include=["metadatas"])
        existing = set()
        if all_records and all_records.get("metadatas"):
            for meta in all_records["metadatas"]:
                if meta and "digest_id" in meta:
                    existing.add(str(meta["digest_id"]))
        return existing

chroma_store = ChromaVectorStore()
