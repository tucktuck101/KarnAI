# Karn.AI Proof of Concept (POC) Scope

## Purpose
The **Proof of Concept (POC)** demonstrates feasibility and establishes the foundation for Karn.AI.  

---

## In Scope
- Precon decklists up to 22/09/2025.  
- Simulation of 4-player pods with deterministic seeds for reproducibility.  
- Rule compliance with Comprehensive Rules (digital-playable subset).  
- Baseline bot using seeded randomisation for deterministic test automation.  
- Early RL agent training experiments.  
- Replay logging and deck power convergence analysis.  

---

## Out of Scope
- Physical-only card effects (e.g., Chaos Orb, dexterity cards).  
- Paid cloud infrastructure (must run on limited local hardware).  
- Fully optimized RL training at production scale.  

---

## POC Success Criteria
- ✅ A working simulation engine that can complete full pod games.  
- ✅ Decklists validated into CardIR format.  
- ✅ Basic bot capable of deterministic test automation.  
- ✅ Initial RL agents showing archetype-aware play patterns.  
- ✅ Convergence of deck rankings across repeated simulations.  
- ✅ Logs, replays, and metrics available for inspection.  
