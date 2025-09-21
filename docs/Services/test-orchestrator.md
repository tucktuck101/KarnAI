test-orchestrator.txt

Test Orchestrator
=================

Purpose:
--------
The `test-orchestrator` coordinates and executes automated tests across the entire system, ensuring simulation integrity, service availability, schema correctness, and agent behavior under various scenarios.

Responsibilities:
-----------------
- Run unit, integration, and end-to-end tests across services.
- Validate schema conformance for IRs, replays, and logs.
- Simulate edge cases, failure conditions, and infinite loop detection.
- Support pre-deployment and continuous integration testing pipelines.

Key Features:
-------------
- Supports test modes: local, staging, CI.
- Tracks test coverage and logs regressions.
- Includes gameplay correctness scenarios using known card interactions.
- Validates reward accuracy and convergence checks.

Inputs:
-------
- Simulation test cases (decklists, seed values, actions)
- Card IR validation rules
- Expected game state outcomes and reward deltas
- Test definitions per service (via YAML or JSON)

Outputs:
--------
- Test pass/fail reports (JSON, JUnit format)
- Regression warnings or breakage flags
- Metrics on performance, latency, and agent response times
- Optional replay logs for visual inspection

Execution Flow:
---------------
1. Load registered test suites and targets
2. Launch test simulations with predefined inputs
3. Compare outputs (placement, reward, replay trace) to expectations
4. Log and publish results
5. Flag anomalies for review

Integration Points:
-------------------
- Launches `simulation-engine` in test mode
- Pulls IRs from `card-ir-registry`
- Verifies reward outputs from `reward-shaping-agent`
- Checks replay integrity via `replay-logger`
- May report results to `ci-cd` pipeline and dashboard

Deployment:
-----------
- Runs as a CLI or microservice
- Included in GitHub Actions or other CI/CD workflows
- Optional nightly regression test runner in production/staging

The `test-orchestrator` ensures simulation correctness, early bug detection, and system confidence for long-running and reproducible agent training.
