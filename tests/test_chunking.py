"""Tests for text chunking module."""
import pytest
from src.pipeline.chunk_text import chunk_text


def test_chunk_basic():
    """Test basic chunking."""
    text = "This is a test sentence for chunking purposes."
    chunks = chunk_text(text, max_size=20)
    assert len(chunks) > 1


def test_chunk_overlap():
    """Test chunking with overlap."""
    text = "The quick brown fox jumps over the lazy dog."
    chunks = chunk_text(text, max_size=15, overlap=5)
    # Check overlap exists


def test_chunk_empty():
    """Test chunking empty text."""
    result = chunk_text("")
    assert result == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
