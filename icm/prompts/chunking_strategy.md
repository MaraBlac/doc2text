# Chunking Strategy Prompt

## Task
Split text into logical chunks for processing.

## Strategies
- **semantic**: Split on paragraphs and sentences
- **fixed**: Split at fixed character count
- **topic**: Split on topic transitions

## Parameters
- max_chunk_size: Maximum chunk size (tokens/characters)
- overlap: Number of characters to overlap between chunks
- min_chunk_size: Minimum chunk size before splitting
