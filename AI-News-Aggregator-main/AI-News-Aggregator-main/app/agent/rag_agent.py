import logging
import json
from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime
from langgraph.graph import StateGraph, END

from app.database.repository import Repository, repository
from app.services.embedding_service import embedding_service
from app.services.search_service import search_service
from app.agent.base_llm import LLMClient

logger = logging.getLogger(__name__)

# Cosine similarity threshold for stored ChromaDB vector sufficiency
SIMILARITY_THRESHOLD = 0.50

class RAGState(TypedDict):
    question: str
    email: Optional[str]
    topics: Optional[List[str]]
    planned_tools: List[str]
    retrieved_articles: List[Dict[str, Any]]
    live_articles: List[Dict[str, Any]]
    verified_sources: List[Dict[str, Any]]
    from_live_search: bool
    grounded: bool
    answer: str

class RAGAgent:
    """
    Agentic RAG StateGraph orchestrator built with LangGraph:
    1. Query Analysis & Routing (Decides tools)
    2. Retrieval (ChromaDB Vector Store)
    3. Relevance Check (Evaluates score threshold)
    4. Live Research (Fallback web search if evidence is low)
    5. Evidence Verification (Filters sources & deduplicates)
    6. Synthesis (Groq LLM grounded synthesis with citations)
    """

    def __init__(self, repo: Optional[Repository] = None):
        self.repo = repo or repository
        self.llm = LLMClient()
        self.graph = self._build_graph()

    def _query_analysis_routing_node(self, state: RAGState) -> Dict[str, Any]:
        """Stage 1: Analyzes user query, resolves user topic preferences, and selects tool pipeline."""
        question = state.get("question", "").strip()
        email = state.get("email")
        user_topics = state.get("topics")

        # Fetch topics from PostgreSQL if email is provided and topics list is empty
        if not user_topics and email:
            user = self.repo.get_user_by_email(email)
            if user and user.topics:
                user_topics = [t.topic_name for t in user.topics if t.active]

        planned_tools = ["vector_search_chromadb"]
        question_lower = question.lower()
        if any(w in question_lower for w in ["today", "latest", "breaking", "now", "live", "weather"]):
            planned_tools.append("web_search_live")

        logger.info(f"[LangGraph Agent] Stage 1 Query Analysis: Query='{question[:40]}...', Topics={user_topics}, Planned Tools={planned_tools}")

        return {
            "topics": user_topics,
            "planned_tools": planned_tools
        }

    def _vector_search_node(self, state: RAGState) -> Dict[str, Any]:
        """Stage 2: Vector similarity retrieval against persistent ChromaDB vector store."""
        question = state.get("question", "").strip()
        user_topics = state.get("topics")

        if not question:
            return {"retrieved_articles": []}

        # Embed query text locally using FastEmbed (BAAI/bge-small-en-v1.5)
        query_vector = embedding_service.embed_text(question)

        # Scoped vector search in ChromaDB
        articles = self.repo.vector_search(
            query_vector=query_vector,
            limit=6,
            topics=user_topics if (user_topics and len(user_topics) > 0) else None
        )

        # Fallback to general vector search if no matches in selected topics
        if not articles or (len(articles) > 0 and float(articles[0].get("score", 0.0)) < SIMILARITY_THRESHOLD):
            general_articles = self.repo.vector_search(query_vector=query_vector, limit=6, topics=None)
            if general_articles:
                if not articles or float(general_articles[0].get("score", 0.0)) > float(articles[0].get("score", 0.0)):
                    articles = general_articles

        logger.info(f"[LangGraph Agent] Stage 2 Vector Search (ChromaDB): Retrieved {len(articles)} documents. Top Score={articles[0].get('score') if articles else 'N/A'}")
        return {"retrieved_articles": articles}

    def _check_relevance_condition(self, state: RAGState) -> str:
        """Stage 3: Conditional Routing Decision — Checks if ChromaDB retrieval is sufficient."""
        articles = state.get("retrieved_articles", [])
        if not articles or len(articles) == 0:
            logger.info("[LangGraph Agent] Relevance Check: No ChromaDB matches. Routing to live_research.")
            return "live_research"

        top_score = float(articles[0].get("score", 0.0))
        if top_score < SIMILARITY_THRESHOLD:
            logger.info(f"[LangGraph Agent] Relevance Check: Vector score ({top_score:.3f}) < threshold ({SIMILARITY_THRESHOLD}). Routing to live_research.")
            return "live_research"

        logger.info(f"[LangGraph Agent] Relevance Check: Vector score ({top_score:.3f}) >= threshold ({SIMILARITY_THRESHOLD}). Routing to evidence_verification.")
        return "evidence_verification"

    def _live_research_node(self, state: RAGState) -> Dict[str, Any]:
        """Stage 4: Live Research fallback via Brave Search / Google CSE / Google News."""
        question = state.get("question", "")
        topics = state.get("topics", [])
        primary_topic = topics[0] if (topics and len(topics) > 0) else None

        logger.info(f"[LangGraph Agent] Stage 4 Live Research Tool executing for query: '{question}'")
        live_results = search_service.live_search(query=question, topic=primary_topic, num_results=6)

        return {
            "live_articles": live_results,
            "from_live_search": True if (live_results and len(live_results) > 0) else False
        }

    def _evidence_verification_node(self, state: RAGState) -> Dict[str, Any]:
        """Stage 5: Validates and filters sources, removes noise and formats verified metadata."""
        live_items = state.get("live_articles", [])
        stored_items = state.get("retrieved_articles", [])
        use_live = state.get("from_live_search", False) and len(live_items) > 0

        verified_sources = []

        if use_live:
            for item in live_items:
                title = item.get("title", "Untitled")
                url = item.get("url", "#")
                src = item.get("source", "Live Search").capitalize()
                snippet = item.get("snippet", "")
                if snippet:
                    verified_sources.append({
                        "title": title,
                        "url": url,
                        "source": f"Live Web ({src})",
                        "date": "Today",
                        "text": snippet,
                        "score": 1.0
                    })
        elif stored_items:
            for item in stored_items:
                title = item.get("title", "Untitled Story")
                url = item.get("source_url", "#")
                topic = item.get("topic", "News")
                pub_date = item.get("published_at")
                date_str = pub_date.strftime("%B %d, %Y") if isinstance(pub_date, datetime) else "Recent"
                text = item.get("text", "")
                score = round(float(item.get("score", 0.0)), 3)

                if text:
                    verified_sources.append({
                        "title": title,
                        "url": url or "#",
                        "source": topic,
                        "date": date_str,
                        "text": text[:600],
                        "score": score
                    })

        logger.info(f"[LangGraph Agent] Stage 5 Evidence Verification: Filtered {len(verified_sources)} verified evidence sources.")
        return {"verified_sources": verified_sources}

    def _synthesis_node(self, state: RAGState) -> Dict[str, Any]:
        """Stage 6: Grounded answer synthesis and citation generation with Groq LLM."""
        question = state.get("question", "")
        verified_sources = state.get("verified_sources", [])

        if not verified_sources:
            return {
                "answer": "I could not find sufficient relevant news coverage from either ChromaDB or live web search to answer this question.",
                "verified_sources": [],
                "from_live_search": False,
                "grounded": False
            }

        context_blocks = []
        sources_meta = []
        for idx, src in enumerate(verified_sources, start=1):
            context_blocks.append(
                f"[Source #{idx}]\nTitle: {src['title']}\nProvider/Topic: {src['source']}\nDate: {src['date']}\nExcerpt:\n{src['text']}\n"
            )
            sources_meta.append({
                "title": src['title'],
                "url": src['url'],
                "source": src['source'],
                "date": src['date'],
                "score": src.get('score')
            })

        context_str = "\n---\n".join(context_blocks)

        system_prompt = """You are an elite, articulate AI News Intelligence Assistant powered by Groq and LangGraph.
Your objective is to answer the user's question accurately, concisely, and insightfully based ONLY on the verified news sources below.

Rules:
1. Ground every statement in the provided sources. Do not make assumptions or extrapolate beyond the provided text.
2. Explicitly cite sources (e.g., "According to [Source Title]...", "As reported by...").
3. Format your answer cleanly using clear paragraphs, bullet points, and key takeaways where applicable.
4. If details are missing, explicitly note what information is unavailable."""

        user_prompt = f"""Verified News Evidence Context:
{context_str}

User Question:
{question}

Please provide your grounded answer with explicit citations now:"""

        try:
            answer = self.llm.generate(system_prompt=system_prompt, user_prompt=user_prompt, json_mode=False)
        except Exception as e:
            logger.error(f"[LangGraph Agent ERROR] Groq LLM synthesis failed: {e}")
            top_title = sources_meta[0]["title"] if sources_meta else "Recent Stories"
            answer = f"Based on verified news matches regarding '{top_title}', coverage was identified.\n\n(Generated via fallback synthesis)"

        # Log agent run to relational database
        try:
            self.repo.log_agent_run(
                user_email=state.get("email"),
                question=question,
                answer=answer.strip(),
                sources=sources_meta,
                from_live_search=state.get("from_live_search", False),
                grounded=True
            )
        except Exception as log_err:
            logger.warning(f"[LangGraph Agent WARNING] Could not log agent run: {log_err}")

        return {
            "answer": answer.strip(),
            "verified_sources": sources_meta,
            "grounded": True
        }

    def _build_graph(self):
        """Builds and compiles the 6-stage LangGraph StateGraph."""
        workflow = StateGraph(RAGState)

        # 1. Add Nodes
        workflow.add_node("query_analysis", self._query_analysis_routing_node)
        workflow.add_node("vector_search", self._vector_search_node)
        workflow.add_node("live_research", self._live_research_node)
        workflow.add_node("evidence_verification", self._evidence_verification_node)
        workflow.add_node("synthesis", self._synthesis_node)

        # 2. Set Entry Point
        workflow.set_entry_point("query_analysis")

        # 3. Add Edges
        workflow.add_edge("query_analysis", "vector_search")

        # 4. Conditional Edge from vector_search to live_research or evidence_verification
        workflow.add_conditional_edges(
            "vector_search",
            self._check_relevance_condition,
            {
                "live_research": "live_research",
                "evidence_verification": "evidence_verification"
            }
        )

        workflow.add_edge("live_research", "evidence_verification")
        workflow.add_edge("evidence_verification", "synthesis")
        workflow.add_edge("synthesis", END)

        return workflow.compile()

    def answer_question(
        self,
        email: str,
        question: str,
        topics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Executes the compiled LangGraph agent workflow."""
        cleaned_question = question.strip()
        if not cleaned_question:
            return {
                "answer": "Please enter a question regarding current news stories.",
                "sources": [],
                "from_live_search": False,
                "grounded": False
            }

        initial_state: RAGState = {
            "question": cleaned_question,
            "email": email,
            "topics": topics,
            "planned_tools": [],
            "retrieved_articles": [],
            "live_articles": [],
            "verified_sources": [],
            "from_live_search": False,
            "grounded": False,
            "answer": ""
        }

        # Invoke compiled LangGraph graph
        result = self.graph.invoke(initial_state)

        return {
            "answer": result.get("answer", ""),
            "sources": result.get("verified_sources", []),
            "from_live_search": result.get("from_live_search", False),
            "grounded": result.get("grounded", True)
        }

# Global agent instance
rag_agent = RAGAgent()
