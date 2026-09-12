import pytest
from app.services.embedding_service import embedding_service
from app.database.repository import repository

def test_embedding_dimensions_and_similarity():
    """Verify that FastEmbed produces 384-dimensional vectors and cosine similarity works."""
    text1 = "OpenAI releases new GPT-5 model with enhanced reasoning capabilities."
    text2 = "Artificial intelligence LLMs and reasoning neural networks."
    text3 = "Cricket tournament results: India beats Australia in World Cup final."

    v1 = embedding_service.embed_text(text1)
    v2 = embedding_service.embed_text(text2)
    v3 = embedding_service.embed_text(text3)

    assert len(v1) == 384, f"Expected 384 dimensions, got {len(v1)}"
    assert len(v2) == 384
    assert len(v3) == 384

    sim_ai = embedding_service.cosine_similarity(v1, v2)
    sim_cross = embedding_service.cosine_similarity(v1, v3)

    print(f"\n[TEST] AI-to-AI similarity: {sim_ai:.4f}")
    print(f"[TEST] AI-to-Cricket similarity: {sim_cross:.4f}")

    assert sim_ai > sim_cross, f"Expected AI-to-AI similarity ({sim_ai}) > AI-to-Cricket ({sim_cross})"
    assert sim_ai > 0.5, "Expected high semantic similarity for related topics"

def test_chromadb_vector_search_retrieval():
    """Verify vector search against stored ChromaDB vector collection."""
    from app.database.chroma import chroma_store
    from app.services.embedding_service import embedding_service
    count = chroma_store.collection.count()
    assert count >= 0

    query_text = "cricket match series score and tournament update"
    query_vec = embedding_service.embed_text(query_text)
    results = chroma_store.vector_search(query_vec, limit=3)
    assert isinstance(results, list)

