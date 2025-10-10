# Stage 12 — Replay logging and viewer

Format: **JSON Lines**

- Header:
  ```json
  {"type":"header","seed":123,"config":{...},"created_at": 1730000000.0}
  ```
- Step:
  ```json
  {"type":"step","idx":0,"action":{"type":"pass_priority"},"obs":{"turn":1,...}}
  ```
- Footer:
  ```json
  {"type":"footer","sha256":"..."}  // computed from engine.snapshot()
  ```

APIs:
- `ReplayLogger`: write replays to `.replay.jsonl`
- `iter_replay(path)`: yield parsed events
- `render_text(path, limit=None)`: produce a text summary for CLI/CI
