# Stage 9 — CLI Runner Integration

Purpose:
Provide a top-level command-line interface to run training sessions, evaluate policies, and inspect logs.

Implements `karnai.cli.karnai.py` entrypoint with Click.

Commands:
- `setup`: ensures venv and structure (placeholder)
- `train`: runs evaluation harness between two policies
- `repl`: opens interactive debug shell for environment stepping
