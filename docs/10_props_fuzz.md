# Stage 5b — Property-based and Fuzz Testing

Focus: invariants for determinism and basic engine/state safety using Hypothesis.

Initial invariants
- Determinism: Same seed + same action sequence => identical snapshot hash.
- Priority rotation: `pass_priority` advances priority in modulo-4; after a full cycle, active player increments.
- Log monotonicity: event count never decreases.
