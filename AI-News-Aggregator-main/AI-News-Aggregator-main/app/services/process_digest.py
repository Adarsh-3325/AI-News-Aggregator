from typing import Optional
from app.database.repository import Repository, repository
from app.agent.digest_agent import DigestAgent

def process_unprocessed_digests(repo: Optional[Repository] = None, limit: int = 10) -> int:
    """Fetches unprocessed raw articles from database and generates LLM summaries + ChromaDB vector embeddings."""
    repo = repo or repository
    unprocessed_articles = repo.get_unprocessed_articles()

    if not unprocessed_articles:
        print("   [INFO] No unprocessed articles to summarize.")
        return 0

    to_process = unprocessed_articles[:limit]
    print(f"   Processing {len(to_process)} article(s) with Groq LLM...")

    agent = DigestAgent()
    processed_count = 0

    for article in to_process:
        if isinstance(article, dict):
            source = article.get("source", "unknown")
            title = article.get("title", "Untitled")
            raw_content = article.get("raw_content", "")
            category = article.get("category", "general")
            topic_name = article.get("topic_name", "General News")
            article_id = article.get("_id") or article.get("id")
            url = article.get("url", "")
            pub_at = article.get("published_at")
        else:
            source = getattr(article, "source", "unknown")
            title = getattr(article, "title", "Untitled")
            raw_content = getattr(article, "raw_content", "")
            category = getattr(article, "category", "general")
            topic_name = getattr(article, "topic_name", "General News")
            article_id = getattr(article, "id")
            url = getattr(article, "url", "")
            pub_at = getattr(article, "published_at")

        safe_title = title.encode('ascii', 'replace').decode('ascii')[:45]
        print(f"   [AI] Summarizing [{source}]: {safe_title}...")
        try:
            # Special fast-path for weather reports
            if source == "open_meteo":
                summary = raw_content.split("\n")[0] if "\n" in raw_content else raw_content
                takeaways = "\n".join([f"- {line.strip()}" for line in raw_content.split("\n")[1:] if line.strip()])
                saved_digest = repo.save_digest(
                    article_id=article_id,
                    summary=summary,
                    key_takeaways=takeaways or "- Check local weather advisories",
                    category="weather",
                    topic_name=topic_name
                )
                digest_id = getattr(saved_digest, "id", None) or saved_digest.get("id") or saved_digest.get("_id")
                processed_count += 1

                # Generate vector embedding for ChromaDB
                try:
                    from app.services.embedding_service import embedding_service
                    embed_text = f"{title}\n{summary}\n{takeaways}"
                    vector = embedding_service.embed_text(embed_text)
                    repo.save_article_embedding(
                        article_id=article_id,
                        digest_id=digest_id,
                        topic=topic_name,
                        title=title,
                        text=embed_text,
                        embedding=vector,
                        source_url=url,
                        published_at=pub_at
                    )
                except Exception as emb_err:
                    print(f"      [WARN] Could not generate embedding for weather: {emb_err}")
                continue

            digest_data = agent.summarize(
                title=title,
                source=source,
                raw_content=raw_content
            )

            # Format takeaways as formatted markdown bullets
            formatted_takeaways = "\n".join([f"- {bullet.lstrip('•-* ')}" for bullet in digest_data.key_takeaways])

            saved_digest = repo.save_digest(
                article_id=article_id,
                summary=digest_data.summary,
                key_takeaways=formatted_takeaways,
                category=category if category != "general" else digest_data.category.lower(),
                topic_name=topic_name
            )
            digest_id = getattr(saved_digest, "id", None) or (saved_digest.get("id") if isinstance(saved_digest, dict) else None)
            processed_count += 1

            # Generate and persist 384-d FastEmbed vector in ChromaDB
            try:
                from app.services.embedding_service import embedding_service
                embed_text = f"{title}\n{digest_data.summary}\n{formatted_takeaways}"
                vector = embedding_service.embed_text(embed_text)
                repo.save_article_embedding(
                    article_id=article_id,
                    digest_id=digest_id,
                    topic=topic_name,
                    title=title,
                    text=embed_text,
                    embedding=vector,
                    source_url=url,
                    published_at=pub_at
                )
            except Exception as emb_err:
                print(f"      [WARN] Could not generate embedding for article ID={article_id}: {emb_err}")

        except Exception as e:
            print(f"   [ERROR] Failed to summarize article ID={article_id}: {e}")

    print(f"   [SUCCESS] Successfully generated {processed_count} digest(s).")
    return processed_count

