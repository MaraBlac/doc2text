"""Tests for text cleaning module."""
import pytest
from src.pipeline.clean_text import clean_text


def test_clean_basic():
    """Test basic text cleaning."""
    text = "  Hello   World  \n\n   Page 1   "
    result = clean_text(text)
    assert "Hello World" in result


def test_clean_unicode():
    """Test unicode normalization."""
    text = "Caf\u00e9"  # Caf\u00e9 with \u00e9
    result = clean_text(text)
    assert "café" in result


def test_clean_page_numbers():
    """Test page number removal."""
    text = "Content text\n\nPage 123\n\nMore content"
    result = clean_text(text)
    # Short lines should be removed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
