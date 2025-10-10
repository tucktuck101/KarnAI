# Karn.AI – Functional Requirements (Comprehensive)

## 1. Introduction
This document specifies the **Functional Requirements (FRs)** for the Karn.AI project, an open-source Gym-style simulator for **Magic: The Gathering – Commander (EDH)**.  
Each FR includes a **specification** and **acceptance criteria (AC)**. Where relevant, rules citations from the **Comprehensive Rules (CR)** are noted for traceability.

---

## 2. Environment & API

**FR-ENV-001: Gym-Compatible API**  
- **Spec:** Provide `reset()`, `step()`, `render()`, `seed()` methods.  
- **AC:** Conforms to OpenAI Gym interface; deterministic outcomes given same seed.  

**FR-ENV-002: Action & Observation Spaces**  
- **Spec:** Define structured action/observation schema: zones, stack, life, commanders, mana, phase, priority, tax/damage tracking.  
- **AC:** `env.action_space` and `env.observation_space` documented; legal-action masking implemented.  

**FR-ENV-003: Render & Hooks**  
- **Spec:** Support JSON/text render for debugging and visualization; expose hooks for replay viewer.  
- **AC:** Render outputs deterministic snapshots; replays identical across runs.  

---

## 3. Data & Deck Management

**FR-DATA-001: Scryfall Data Import**  
- **Spec:** Import card data via Scryfall bulk API with version pinning.  
- **AC:** CLI import succeeds within 2 minutes for current card set.  

**FR-DATA-002: CardIR Generation**  
- **Spec:** Normalize card data into CardIR: tokenization, tags, oracle text.  
- **AC:** CardIR generation deterministic; hash stable across environments.  

**FR-DECK-003: Commander Deck Validation**  
- **Spec:** Enforce Commander legality: 100 cards, singleton (except basics), color identity, commander eligibility.  
- **AC:** Illegal decks rejected with explicit error reason.  

---

## 4. Core Rules Engine

**FR-RULES-004: Turn Structure**  
- **Spec:** Implement CR 500–511 (phases & steps).  
- **AC:** Turn simulation matches CR order; priority passes at each step.  

**FR-RULES-005: Stack & Priority**  
- **Spec:** Implement CR 116 & 601–608; spells/abilities use stack; APNAP ordering.  
- **AC:** Spells resolve in LIFO order; priority windows validated.  

**FR-RULES-006: Targets & Legality**  
- **Spec:** Enforce CR 601.2c–f target rules and legality checks.  
- **AC:** Illegal targets disallowed; validation occurs before stack push.  

**FR-RULES-007: State-Based Actions**  
- **Spec:** Implement CR 704 SBAs.  
- **AC:** SBAs checked after resolution and before priority; test suite passes.  

**FR-RULES-008: Triggered & Static Abilities**  
- **Spec:** Implement CR 603–604 triggered/static abilities.  
- **AC:** Triggers fire when conditions met; static auras/anthems apply continuously.  

**FR-RULES-009: Replacement & Prevention Effects**  
- **Spec:** Implement CR 614–615.  
- **AC:** Replacement choices prompt correctly; prevention modifies events as per CR.  

**FR-RULES-010: Continuous Effects & Layers**  
- **Spec:** Implement CR 613 layer system for P/T, copy, control, text, timestamp.  
- **AC:** Sample scenarios (e.g., pump + base setter) resolve correctly.  

**FR-RULES-011: Illegal Actions & Shortcuts**  
- **Spec:** Implement CR 731–732.  
- **AC:** Illegal actions rewound; shortcut options logged.  

**FR-RULES-012: Keyword Coverage Baseline**  
- **Spec:** Support minimum set: flying, trample, haste, hexproof, ward, menace, deathtouch, lifelink, goad, investigate.  
- **AC:** Test scenarios for each pass. Unsupported keywords gracefully rejected/logged.  

---

## 5. Commander-Specific Rules

**FR-CMD-013: Commander Identity & Tax**  
- **Spec:** Enforce commander color identity and tax (CR 903).  
- **AC:** Casting outside identity blocked; tax increments tracked.  

**FR-CMD-014: Commander Damage**  
- **Spec:** Track 21 damage from individual commanders.  
- **AC:** Player loses if ≥21 from same commander.  

**FR-CMD-015: Commander Variants**  
- **Spec:** Support partner, Background, Doctor’s companion.  
- **AC:** Eligible partners selectable; deck validation enforces rules.  

---

## 6. Multiplayer & Combat

**FR-MP-016: Pod Formation & Starting State**  
- **Spec:** Default 4-player pods; randomized seating; life = 40; London mulligan.  
- **AC:** Game snapshot includes seating, commanders, life totals.  

**FR-MP-017: Attack Multiple Players & Planeswalkers**  
- **Spec:** Implement CR 802 attack rules.  
- **AC:** Legal attacker/defender selection enforced.  

**FR-MP-018: Blockers & Requirements**  
- **Spec:** Enforce menace, must-block, and multi-blocking legality.  
- **AC:** Blocking scenarios validated via tests.  

**FR-MP-019: Range of Influence (optional)**  
- **Spec:** Allow limited range of influence toggle (CR 801).  
- **AC:** Test passes if feature enabled/disabled.  

---

## 7. Reinforcement Learning Integration

**FR-RL-020: Agent Action Interface**  
- **Spec:** Expose action masking, legal move set, and policy hooks.  
- **AC:** RLlib policy consumes valid moves; illegal moves masked.  

**FR-RL-021: Rewards & Episode Termination**  
- **Spec:** Expose rewards: win/loss, partial rewards (commander tax, damage dealt).  
- **AC:** Episode ends on win condition; rewards align with outcome.  

---

## 8. Replay & Logging

**FR-REPLAY-022: Deterministic Replays**  
- **Spec:** Serialize full game state and RNG seed.  
- **AC:** Replay execution identical to original run.  

**FR-REPLAY-023: Event Logs & Explanations**  
- **Spec:** Log all events (stack, priority, SBAs, commander tax) with rule references.  
- **AC:** Replay viewer reconstructs timeline; explanation-service consumes logs.  

---

## 9. Performance & Determinism

**FR-PERF-024: Simulation Throughput**  
- **Spec:** Support ≥500 steps/minute on reference hardware (CPU-only).  
- **AC:** Benchmark suite validates speed.  

**FR-PERF-025: Determinism Across Environments**  
- **Spec:** Identical inputs + seed produce identical outputs across OS/platform.  
- **AC:** Cross-platform test harness passes.  

---

## 10. Extensibility & Modularity

**FR-EXT-026: Modular Keyword/Ability Loader**  
- **Spec:** Keywords implemented as modular handlers with fallback logging.  
- **AC:** Unsupported keyword gracefully logged without crash.  

**FR-EXT-027: Plugin Architecture for Agents & Rules**  
- **Spec:** Agent-service and rules modules pluggable.  
- **AC:** New agents/rules loadable without core modification.  
