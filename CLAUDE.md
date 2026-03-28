# Claude Code Configuration

## Guidelines

- Always read existing code before modifying
- Prefer editing existing files over creating new ones
- Keep implementations simple and focused
- Write secure, tested code

## Architecture

- Use `pipeline/orchestrator.py` to coordinate processing steps
- Externalize configuration via YAML files in `configs/`
- Store embeddings cache in `icm/memory/`

## Notes

- PDF extraction prompts are in `icm/prompts/`
- Logging configuration in `configs/logging.yaml`
- Pipeline settings in `configs/pipeline.yaml`
