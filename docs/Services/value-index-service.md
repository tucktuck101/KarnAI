value-index-service.txt

Value Index Service
===================

Purpose:
--------
The `value-index-service` compares the performance of individual cards and decks in simulation to their financial cost, enabling analysis of efficiency, over/undervaluation, and budget competitiveness.

Responsibilities:
-----------------
- Aggregate per-card performance data from simulations.
- Ingest real-time price data from secondary markets.
- Normalize performance metrics across archetypes and formats.
- Produce financial efficiency scores and trend reports.
- Serve value indexes to dashboards and external APIs.

Key Features:
-------------
- Computes cost-to-impact ratio at the card and deck level.
- Tracks over- and underperforming cards by price tier.
- Integrates with reward shaping to calculate composite value metrics.
- Exposes trend data for future meta and pricing predictions.

Inputs:
-------
- Card reward impact data (from `reward-shaping-agent`)
- Game result statistics (from `result-aggregator`)
- Card prices (from `price-ingestor`)
- Card metadata and IRs (from `card-ir-registry`)

Outputs:
--------
- Financial efficiency scores per card and deck
- Impact-adjusted price index reports
- Historical performance vs. price plots
- API and dashboard data for public transparency

Execution Flow:
---------------
1. Fetch latest price data from `price-ingestor`
2. Join with reward statistics and game impact logs
3. Normalize per-card efficiency scores (e.g., impact / cost)
4. Store value indexes and trends
5. Emit updates to dashboards and report generators

Integration Points:
-------------------
- Reads from:
   - `reward-shaping-agent` (impact values)
   - `result-aggregator` (win rates)
   - `price-ingestor` (cost data)
   - `card-ir-registry` (card metadata)
- Serves data to `public-webpage` and external analysts

Deployment:
-----------
- Python or Go service optimized for financial analysis
- Runs as a batch job or streaming service
- Data stored in PostgreSQL or MongoDB with caching layer

The `value-index-service` provides actionable insights into the true worth of cards and decks, powering budget optimization, meta efficiency tools, and potential monetization opportunities.
