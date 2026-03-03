# Planning: Yelp AI Assistant (Production Mirror)

This document outlines the roadmap to replicate the exact "Yelp Assistant" production architecture as described in the ByteByteGo reference. The goal is to mirror the high-scale, multi-stage RAG system used at Yelp.

## Phase 1: Production-Grade Data Indexing (Offline)
*Goal: Build the dual-store architecture for structured and unstructured data.*

1.  **Structured Data Store (Cassandra)**:
    *   Implement an **Entity-Attribute-Value (EAV)** layout for business attributes (hours, "heated patio", "vegan options").
    *   *Why*: Allows schema flexibility without migrations and high-scale reads.
2.  **Unstructured Search Index (Elasticsearch/Lucene)**:
    *   Index review snippets and photo captions into a Lucene-based engine.
    *   Configure for **Hybrid Retrieval**: Combine BM25 keyword matching with vector embeddings for semantic search.
3.  **Data Ingestion Pipeline**:
    *   Script to transform `yelp_academic_dataset_business.json` into EAV rows.
    *   Script to chunk `yelp_academic_dataset_review.json` into searchable snippets.

## Phase 2: The Content Fetching API (Abstraction Layer)
*Goal: Decouple the assistant logic from the storage details.*

1.  **Unified Interface**:
    *   Create a internal API service that parallelizes requests to Cassandra (Facts) and Elasticsearch (Reviews/Photos).
2.  **Latency Management**:
    *   Implement strict latency budgets (aiming for sub-100ms retrieval).
    *   Handle parallel fetching using `asyncio` in Python.

## Phase 3: The Specialized Analysis Pipeline
*Goal: Deconstruct the "Monolithic LLM" into fast, tiered models.*

1.  **Safety & Intent (Tiered - Small Model)**:
    *   **Trust & Safety Classifier**: Block adversarial/unsafe inputs early.
    *   **Inquiry Type Classifier**: Redirect out-of-scope questions (e.g., "how to reset password").
2.  **Strategic Routing (Tiered - Small Model)**:
    *   **Content Source Selector**: Analyze intent to route queries to either Cassandra (Facts) or Elasticsearch (Subjective content).
    *   **Keyword Generator**: Translate natural language (e.g., "vibe") into optimized search terms (e.g., "atmosphere", "decor").

## Phase 4: Evidence-Grounded Generation
*Goal: Synthesize answers with strict citations.*

1.  **Final Generation (Large Model - GPT-4o)**:
    *   Feed only relevant snippets from the Content Fetching API.
    *   Enforce a strict "Answer only from context" policy.
2.  **Citation Verification**:
    *   A post-processing step to ensure markers (e.g., [S1]) map to real, retrievable snippets.

## Phase 5: High-Performance Serving
*Goal: Low-latency, responsive user experience.*

1.  **Streaming (FastAPI + SSE)**:
    *   Use Server-Sent Events to stream tokens to the UI in real-time.
2.  **Early Stopping**:
    *   If the Safety Classifier flags a query, cancel all downstream retrieval and generation immediately to save compute.

---

## Technical Stack Mirror
*   **Structured Store**: Cassandra (or ScyllaDB for local dev).
*   **Unstructured Store**: Elasticsearch / OpenSearch (Lucene-based).
*   **Backend**: FastAPI (Asynchronous).
*   **Models**: 
    *   *Analysis*: Small, fine-tuned or efficient models (e.g., GPT-4o-mini).
    *   *Synthesis*: Large, reasoning models (e.g., GPT-4o).
*   **Communication**: Server-Sent Events (SSE).

---

## Next Steps (Immediate)
1. [ ] Set up local Docker environment for **Cassandra** and **Elasticsearch**.
2. [ ] Write the EAV transformation script for business attributes.
3. [ ] Build the initial "Inquiry Classifier" prompt/logic.
