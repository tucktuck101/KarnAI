# Stage 6 — Card Ability DSL & IR

Goal: Provide a minimal, testable path from **Oracle text** → **IR** → callable effect stubs.

## IR Overview
```json
{
  "cost": {"tap_self": true},
  "ops": [
    {"op": "add_mana", "color": "G", "amount": 1}
  ],
  "text": "{T}: Add {G}."
}
```

Another example:
```json
{
  "cost": null,
  "ops": [
    {"op": "counter_target", "target": "spell"}
  ],
  "text": "Counter target spell."
}
```

The IR is intentionally simple. It is **not** a full rule engine. It feeds the engine with concrete intent.
