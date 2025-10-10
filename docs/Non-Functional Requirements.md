# Karn.AI – Non-Functional Requirements (Comprehensive)

This document defines the **Non-Functional Requirements (NFRs)** for Karn.AI.  
They are derived from **ISO/IEC 25010**, **SRE principles**, the project vision, and technical constraints.

---

## NFR-PERF-001: Simulation Performance
**Quality Attribute:** Performance/Throughput  
**Measure:** Step latency (95th percentile)  
**Target:** ≤ 10 ms per step on CPU (i7-4770, 8GB, GTX 1080Ti optional).  
**Method:** Benchmark test in CI.  
**Scope:** simulation-engine, agent-service.  
**Linked FRs:** FR-ENV-001, FR-RULES-004.  

---

## NFR-REL-002: Crash Recovery
**Quality Attribute:** Reliability/Availability  
**Measure:** MTTR (Mean Time to Recovery)  
**Target:** ≤ 2 minutes for engine restart and replay recovery.  
**Method:** Chaos test in CI.  
**Scope:** simulation-engine, replay-logger.  
**Linked FRs:** FR-ENV-001, FR-RULES-007.  

---

## NFR-REPRO-003: Deterministic Reproducibility
**Quality Attribute:** Reproducibility  
**Measure:** Same seed → identical replay log.  
**Target:** 100% consistency across 100 runs.  
**Method:** CI test: run 100 games with same seed, compare logs.  
**Scope:** All services.  
**Linked FRs:** FR-ENV-001, FR-RULES-004, FR-RULES-005.  

---

## NFR-PORT-004: Portability
**Quality Attribute:** Portability  
**Measure:** Environment compatibility  
**Target:** Must run without GPU on Linux/macOS.  
**Method:** CI matrix tests.  
**Scope:** All core services.  
**Linked FRs:** FR-ENV-001.  

---

## NFR-SEC-005: Security
**Quality Attribute:** Security  
**Measure:** Secrets management & repo hygiene  
**Target:** No secrets in repo; CI scans pass.  
**Method:** gitleaks and GitHub secret scanning.  
**Scope:** Repo + CI/CD.  
**Linked FRs:** All.  

---

## NFR-DOC-006: Contributor Onboarding
**Quality Attribute:** Usability/Documentation  
**Measure:** Quickstart setup time  
**Target:** ≤ 10 minutes for new contributor to run first simulation.  
**Method:** Manual timed test + CI docs test.  
**Scope:** Documentation, CLI, Dockerfiles.  
**Linked FRs:** FR-CLI-003, FR-DATA-002.  

---

## NFR-OBS-007: Observability
**Quality Attribute:** Observability/Monitorability  
**Measure:** Metrics + traces coverage  
**Target:** All services emit OTel traces with run_id, seed; Prometheus metrics for steps/sec, illegal_action_rate, convergence.  
**Method:** CI integration test.  
**Scope:** All microservices.  
**Linked FRs:** FR-ENV-001, FR-RULES-004, FR-RULES-007.  

---

## NFR-MAINT-008: Maintainability & Modularity
**Quality Attribute:** Maintainability  
**Measure:** Code complexity & test coverage  
**Target:** 80% test coverage; cyclomatic complexity ≤ 10 for core modules.  
**Method:** CI lint + coverage reports.  
**Scope:** simulation-engine, agent-service, replay-logger.  
**Linked FRs:** All.  

---

## NFR-SCALE-009: Scalability
**Quality Attribute:** Scalability  
**Measure:** Simulation throughput with distributed workers  
**Target:** Linear scaling up to 32 workers with ≤ 10% performance loss per doubling.  
**Method:** Load test with Kubernetes cluster.  
**Scope:** simulation-engine, matchmaker, agent-service.  
**Linked FRs:** FR-ENV-001, FR-MATCH-017.  

---

## NFR-COMP-010: Compliance & Licensing
**Quality Attribute:** Compliance  
**Measure:** Alignment with WOTC Fan Content Policy and OSS licenses.  
**Target:** 100% compliance; no proprietary assets bundled.  
**Method:** Manual audit.  
**Scope:** Repo + documentation.  
**Linked FRs:** All.  
