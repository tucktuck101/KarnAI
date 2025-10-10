# Karn.AI Vision Document

## 1. Purpose
Karn.AI exists to address the **Power Level Problem** in Magic: The Gathering’s Commander (EDH) format.  
By simulating 4-player pods with AI agents and data-driven evaluation, Karn.AI provides **objective, repeatable, and explainable insights** into deck strength, archetype matchups, and gameplay balance.

---

## 2. Vision Statement
*Karn.AI will be the first **open-source Gym environment** for training AI to play Magic: The Gathering — enabling fairer gameplay, deeper game analytics, and providing a baseline metric for comparing deck power levels.*  

---

## 3. Overall Goals
- **Quantify Commander deck power** using simulations, archetype tagging, and performance metrics.  
- **Enable balanced pod construction** by matching decks of equivalent strength.  
- **Provide transparency** through replays, logs, and explainable AI decisions.  
- **Bridge casual and competitive play** with tools relevant to jank brewers, tuned deck players, and cEDH pilots alike.  
- **Support research and experimentation** with an **OpenAI Gym–style API** for reproducible training loops.  
- **Foster a community-driven ecosystem** where contributors extend agents, decks, and analytics modules.  

---

## 4. Long-Term Success Criteria
- ✅ Standardized Gym-compatible API for agent training.  
- ✅ Multi-agent reinforcement learning with archetype-informed strategies.  
- ✅ Distributed simulation framework with community-contributed compute.  
- ✅ Integration with comprehensive MTG datasets (decklists, metagame, card-level analytics).  
- ✅ Explainable AI with replay viewer, visualization, and insight tools.  
- ✅ Recognized baseline metric for deck power in the Commander community.  

---

## 5. Constraints & Assumptions
- Compliance: Must follow WOTC Fan Content Policy.  
- Community: **External contributors are encouraged, but POC is solo-dev.**  
- Open Source: MIT License, modular microservices, transparent processes.  
- Hardware constraints apply for early development (local POC).  

---

## 6. Stakeholders (High-Level)
- **Deckbuilders & Players** → want fair and fun pod experiences.  
- **Researchers** → need reproducible simulations for analysis.  
- **Community Contributors** → interested in extending agents, decks, or data.  
- **Developer (you)** → needs a modular, testable architecture with clear milestones.  

---

## 7. Domain Concepts (Glossary Snapshot)
- **CardIR** → hierarchical tag-based representation of card text.  
- **Archetype Tags** → strategic roles (e.g., ramp, control, stax, combo).  
- **Replay** → full game log, indexable and annotatable.  
- **Reward Shaping** → reinforcement learning feedback aligned to archetype utility.  
- **Bayesian Convergence** → statistical confidence measure for deck power rankings.  
