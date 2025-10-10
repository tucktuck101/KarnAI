# Karn.AI Glossary

This glossary defines key terms for contributors, researchers, and players engaging with Karn.AI.

---

## A) Magic Rules & Commander Terms
- **Object:** Anything the rules recognize on the stack, battlefield, or in zones (spells, abilities, permanents, cards, copies).  
- **Permanent:** An object on the battlefield (artifact, creature, enchantment, land, planeswalker, battle).  
- **Spell:** A card or copy on the stack; resolves into a permanent or effect.  
- **Activated Ability:** Written as “cost: effect”; requires paying a cost.  
- **Triggered Ability:** Written as “when/whenever/at”; goes on the stack automatically.  
- **Static Ability:** Always in effect while the object is present.  
- **Mana Ability:** Adds mana; doesn’t target; resolves immediately under certain conditions.  
- **Special Action:** Actions outside the stack, such as playing a land.  
- **Stack:** Game structure for resolving spells and abilities in last-in-first-out order.  
- **Priority:** The right to act before the stack resolves.  
- **Targeting:** Choosing an eligible object, checked at declaration and resolution.  
- **Replacement Effect:** Modifies an event before it happens.  
- **Prevention Effect:** Prevents a specific event, usually damage.  
- **Continuous Effect:** An effect lasting over time; applied through rule layers.  
- **State-Based Actions:** Automatic checks (e.g., life ≤ 0, lethal damage, legend rule).  
- **Zones:** Library, hand, battlefield, graveyard, exile, stack, and command zone.  
- **Owner:** The player who started with the card in their deck.  
- **Controller:** The player currently controlling the object.  
- **Phases and Steps:** Turn order segments (untap, upkeep, draw, main, combat, second main, end, cleanup).  
- **Commander:** The designated card in the command zone; subject to commander tax and color identity rules.  

---

## B) Simulation Concepts
- **Game State:** Complete snapshot of all zones, objects, effects, and turn information.  
- **Deterministic Seed:** RNG seed ensuring identical outcomes on replay.  
- **Episode:** One complete 4-player game simulation run.  
- **Observation:** Encoded view of the game state for agents.  
- **Action:** A legal decision an agent can make.  
- **Action Mask:** Representation of which actions are legal at a given time.  
- **Environment API:** Gym-style interface with `reset()` and `step(action)`.  
- **Terminal Condition:** Win/loss/draw or forced end (scoop, timeout).  
- **Replay:** Log of all decisions and events in a game.  
- **Judge Trace:** Human-readable explanation of rules interactions.  
- **Illegal Move Policy:** How the system handles invalid agent actions.  

---

## C) CardIR & Data Modeling
- **CardIR:** Hierarchical, tag-based intermediate representation of a card.  
- **IR Operation:** Minimal executable unit derived from CardIR.  
- **Tag:** Normalized label for cards, states, or actions.  
- **Archetype:** A cluster of strategy tags defining a deck’s game plan.  
- **Archetype Biasing:** Using archetype information to guide agent behavior.  
- **DeckIR:** Normalized decklist representation with metadata.  
- **Value Index:** Metric estimating utility of a card or action.  
- **Power Index:** Deck strength measure derived from simulations.  
- **Scryfall Snapshot:** Fixed export of card data by date/hash.  
- **Oracle Text Map:** Mapping of official card text to CardIR templates.  
- **Rules Compatibility Flag:** Marks cards or mechanics excluded from simulation.  

---

## D) Services & Storage
- **simulation-engine:** Core loop executing rules and progressing turns.  
- **agent-service:** Provides policy decisions for agents.  
- **agent-hook:** Sandbox for community or experimental agents.  
- **matchmaker:** Forms pods of decks based on rules and constraints.  
- **replay-logger:** Records games, traces, and metadata.  
- **reward-shaping-agent:** Computes additional reward signals.  
- **bayesian-evaluator:** Monitors convergence of power metrics.  
- **card-ir-generator:** Builds CardIR from Oracle text.  
- **deck-service:** Validates decklists and creates DeckIR.  
- **value-index-service:** Aggregates utility metrics.  
- **explanation-service:** Produces human-readable narratives of actions.  
- **ui-client / replay-viewer / public-webpage:** User interfaces for insights.  

**Storage Components**  
- **Kafka:** Event streaming backbone.  
- **Redis:** Low-latency caching layer.  
- **PostgreSQL:** Relational data storage.  
- **MongoDB:** Document storage for replays.  
- **Neo4j:** Graph database for card and archetype relations.  

---

## E) Machine Learning Concepts
- **Observation Space:** Structured data representing game state.  
- **Action Space:** Legal actions available to the agent.  
- **Reward:** Scalar signal returned to the agent.  
- **Policy:** Mapping from observations to actions.  
- **Shadow Policy:** Parallel model to check for drift.  
- **Opponent Model:** Prediction of other players’ strategies.  
- **Exploration vs Exploitation:** Balancing discovery and optimization.  
- **Curriculum:** Structured training progression.  
- **Evaluation Protocol:** Fixed conditions for model testing.  
- **Convergence Threshold:** Confidence level for power index stabilization.  
- **Sample Efficiency:** Rate of learning relative to number of simulations.  
- **Reproducibility Contract:** Requirements ensuring deterministic runs.  

---

## F) Observability & Operations
- **OpenTelemetry (OTel):** Standard for metrics, traces, and logs.  
- **Trace:** Record of a distributed request across services.  
- **Span:** A single operation within a trace.  
- **Metrics:** Quantitative indicators (e.g., throughput, latency).  
- **Logs:** Structured events for debugging and audits.  
- **SLI / SLO / SLA:** Indicators, objectives, and agreements.  
- **Error Budget:** Allowable threshold of unreliability.  
- **Runbook:** Step-by-step guide for handling incidents.  
- **Helm / Prometheus / Grafana / Loki:** Tools for deployment and observability.  
- **Security Posture:** Standards for secrets, access, and hardening.  
- **Data Retention Policy:** Duration for keeping replays and logs.  

---

## G) Governance & Compliance
- **WotC Fan Content Policy:** Guidelines for creating fan-made content.  
- **MIT License:** Open-source license applied to Karn.AI.  
- **Data Provenance:** Tracking sources and versions of card data.  
- **PII and Privacy:** Handling of sensitive or user-submitted data.  
- **Responsible AI Notes:** Guidelines for ethical and unbiased model behavior.  

---

## H) Project Management
- **Milestone:** Major project checkpoint.  
- **Epic:** Large feature grouping smaller tasks.  
- **Feature:** Distinct system capability.  
- **Task:** Individual unit of work.  
- **User Story:** Format: “As a `<role>`, I want `<capability>` so that `<benefit>`.”  
- **Acceptance Criteria:** Testable definition of done.  
- **Non-Functional Requirement:** Operational quality constraint.  
- **Change Log:** Summary of project modifications.  
