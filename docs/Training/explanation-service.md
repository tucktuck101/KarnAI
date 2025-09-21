explanation-service.txt

Explanation Service
===================

Purpose:
--------
The `explanation-service` provides transparency and interpretability into AI agent decisions within simulations. It captures detailed metadata, strategic tag traces, decision confidence, and rationale behind agent actions to facilitate debugging, training validation, and human understanding.

Responsibilities:
-----------------
- Logs decision-making rationale from `agent-service`, including strategic tag usage, inferred state context, and decision confidence.
- Provides flattened tag traces used by agents for quick and intuitive human understanding.
- Captures shadow policy divergence insights for diagnostic analysis.
- Generates explanations suitable for user-friendly visualization or human annotation.

Key Features:
-------------
- Detailed tracing of strategic tag influence on decision-making.
- Captures confidence scores and exploration parameters used by agents.
- Facilitates human-readable annotations or reviews of agent logic.
- Integrates with `annotation-service` to support human-aided validation.

Inputs:
-------
- Decision data from `agent-service`, including:
  - Flattened strategic tags
  - Confidence scores from RL models
  - State encoding vectors or summaries
  - Bayesian convergence context influencing exploration
- Optional shadow policy divergence metadata.

Outputs:
--------
- Explanation logs with structured, human-readable justification of decisions.
- Tag trace visualizations and decision rationale reports.
- Diagnostic logs highlighting agent behavior trends or anomalies.

Execution Flow:
---------------
1. Receive decision metadata from `agent-service` during simulation.
2. Log structured explanation including tags, confidence, and context.
3. Optionally highlight differences between shadow and primary policy decisions.
4. Provide logs and visualizations to `annotation-service`, dashboards, or analytics pipelines.

Explanation Components:
-----------------------
- Flattened Tag Trace:
  - Clearly lists strategic tags (e.g., ["interaction", "removal", "tempo"]).
  - Supports rapid interpretation of the agent's strategic intent.

- Confidence Scoring:
  - Numeric scores reflecting model confidence in the chosen action.
  - Used to assess decision clarity or agent uncertainty.

- Contextual State Summary:
  - Brief human-readable summaries of relevant state context.
  - Includes key variables like game phase, resources, threats identified, and opponent state.

- Shadow Policy Comparison:
  - Explicit logging of actions taken by parallel shadow policy.
  - Useful for identifying overfitting, stale policies, or exploration issues.

Integration Points:
-------------------
- Receives data directly from `agent-service`.
- Feeds structured logs into `annotation-service` for human auditing.
- Integrates with dashboards (`public-webpage`) and visualization tools (`replay-viewer`).

Deployment:
-----------
- Lightweight, Python-based logging and visualization service.
- Containerized for scalable deployment alongside agent services.
- Optimized for real-time logging and efficient metadata storage.

Conclusion:
-----------
The Explanation Service enhances the transparency, trustworthiness, and auditability of the AI system. By clearly articulating the reasoning behind agent actions, it facilitates robust debugging, continuous training improvements, and greater stakeholder confidence in system outcomes.
