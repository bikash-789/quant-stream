-- Enable pgvector extension for time-indexed embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Table for financial filings and news embeddings with strict timestamp
CREATE TABLE IF NOT EXISTS document_embeddings (
    id BIGSERIAL PRIMARY KEY,
    document_id VARCHAR(128) NOT NULL,
    symbol VARCHAR(16) NOT NULL,
    doc_type VARCHAR(32) NOT NULL,             
    title TEXT,
    chunk_index INT NOT NULL,
    chunk_text TEXT NOT NULL,
    publication_timestamp TIMESTAMPTZ NOT NULL,  -- Point-in-Time filter timestamp -> for look ahead bias
    ingestion_timestamp TIMESTAMPTZ DEFAULT NOW(),
    embedding vector(384)  -- Default dimension for bge-small / all-MiniLM-L6-v2
);

-- Index for fast cosine similarity search
CREATE INDEX IF NOT EXISTS idx_doc_embeddings_hnsw 
ON document_embeddings USING hnsw (embedding vector_cosine_ops);

-- Index for fast point-in-time filtering
CREATE INDEX IF NOT EXISTS idx_doc_pub_time 
ON document_embeddings (publication_timestamp);
