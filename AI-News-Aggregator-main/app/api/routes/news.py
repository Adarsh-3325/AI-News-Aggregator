from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any, Optional
from app.api.schemas import TopicItem, AskQueryRequest, LiveSearchRequest, NewsPreviewRequest
from app.api.services.preview_service import fetch_news_preview
from app.agent.rag_agent import rag_agent
from app.services.search_service import search_service

router = APIRouter(prefix="/api", tags=["News & Agent"])

@router.post("/news/preview", status_code=status.HTTP_200_OK)
async def preview_news_feed(payload: NewsPreviewRequest) -> Dict[str, Any]:
    """Instant live preview endpoint: fetches and summarizes news for selected topics on-demand."""
    if not payload.topics:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one topic must be provided for preview."
        )
    
    parsed_topics = [TopicItem.parse_item(t) for t in payload.topics]
    preview_data = await fetch_news_preview(parsed_topics)
    return preview_data

@router.post("/ask", status_code=status.HTTP_200_OK)
async def ask_agent(payload: AskQueryRequest) -> Dict[str, Any]:
    """LangGraph Agentic RAG endpoint for answering user queries with ChromaDB vector search + live research."""
    try:
        res = rag_agent.answer_question(
            email=payload.email or "",
            question=payload.question,
            topics=payload.topics
        )
        return {
            "status": "success",
            "question": payload.question,
            **res
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent RAG workflow failed: {str(e)}"
        )

@router.post("/search/live", status_code=status.HTTP_200_OK)
async def search_live_news(payload: LiveSearchRequest) -> Dict[str, Any]:
    """Live web search endpoint (Google CSE / Brave Search fallback)."""
    try:
        raw_results = search_service.live_search(
            query=payload.query,
            topic=payload.topic,
            num_results=payload.num_results
        )
        
        formatted_results = []
        for item in raw_results:
            formatted_results.append({
                "title": item.get("title", "Untitled"),
                "summary": item.get("snippet", ""),
                "url": item.get("url", ""),
                "source": item.get("source", "web"),
                "published": item.get("published")
            })

        return {
            "status": "success",
            "query": payload.query,
            "topic": payload.topic,
            "count": len(formatted_results),
            "results": formatted_results
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Live search failed: {str(e)}"
        )
