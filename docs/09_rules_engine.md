# Stage 5 — Rules Engine Kernel (Minimal Deterministic Core)

Purpose: provide a deterministic, seedable kernel with:
- event bus,
- priority/turn scaffold,
- state-based action hook,
- deterministic `snapshot()` for replay bytes.

This is a thin vertical slice to unblock env and CLI tests. Full CR logic comes later.
