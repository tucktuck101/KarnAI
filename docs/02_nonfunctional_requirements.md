# Non-Functional Requirements (NFR)

| ID | Category | Requirement | Target |
|----|-----------|-------------|---------|
| NFR1 | Determinism | Identical seed produces identical replay bytes. | ≥ 99.9 % deterministic runs |
| NFR2 | Performance | Step latency per agent per turn. | ≤ 5 ms on reference hardware |
| NFR3 | Scalability | Horizontal simulation scaling. | Linear up to 10 nodes |
| NFR4 | Reliability | Crash recovery and checkpoint resume. | No data loss on fault |
| NFR5 | Observability | Structured logging and OTel tracing. | 100 % major components instrumented |
| NFR6 | Security | Dependency and license compliance. | 0 critical vulnerabilities |
| NFR7 | Maintainability | Code coverage and lint thresholds. | ≥ 85 % tests, 0 lint errors |
| NFR8 | Portability | Cross-platform execution. | Linux + Windows + macOS |
| NFR9 | Extensibility | New card templates added without core edits. | ≤ 5 LOC change |
| NFR10 | Cost | Local training run affordability. | ≤ 4 CPU + 8 GB RAM baseline |
