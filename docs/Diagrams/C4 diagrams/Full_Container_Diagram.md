flowchart TD
  %% External actors/systems
  subgraph EXT["External"]
    USER[Player or Researcher - Browser]
    COMM[Community Agent Clients]
    SCRY[Scryfall API]
    IDP[OIDC Identity Provider]
  end

  %% System boundary
  subgraph KARNAI["Karn.AI System"]
    subgraph EDGE["Public Edge"]
      INGRESS[Ingress / API Gateway]
      PUBWEB[public-webpage - Next.js]
      UI[ui-client - SPA]
      VIEWER[ui-replay-viewer - SPA]
    end

    subgraph CORE["Core Services"]
      DECK[deck-service - FastAPI]
      CIR[card-ir-generator - Python]
      MATCH[matchmaker - Python]
      SIM[simulation-engine - Python]
      AGENT[agent-service - RLlib Ray]
      HOOK[agent-hook - gRPC sandbox]
      REPLAY[replay-logger - worker]
      EXPL[explanation-service - FastAPI]
      VALUE[value-index-service - FastAPI]
      REWARD[reward-shaping-agent]
      BAYES[bayesian-evaluator]
    end

    subgraph DATA["Data Stores"]
      PG[PostgreSQL - decks ratings indices jobs]
      MONGO[MongoDB - CardIRs replay meta]
      NEO[Neo4j - tags archetype graph]
      REDIS[Redis - cache short queues]
      KAFKA[Kafka - events and streams]
      BLOB[Object Storage - replays checkpoints]
      CFG[Config and Feature Flags]
      KV[Secrets - Key Vault]
    end
  end

  %% External ↔ Edge
  USER --> INGRESS
  USER --> PUBWEB
  USER --> UI
  USER --> VIEWER
  COMM --> HOOK
  INGRESS --> IDP

  %% Edge ↔ Core
  INGRESS --> DECK
  INGRESS --> VALUE
  INGRESS --> EXPL
  INGRESS --> REPLAY
  UI -. uses APIs .-> INGRESS
  VIEWER -. uses APIs .-> INGRESS

  %% Core sync
  DECK --> CIR
  SIM --> AGENT
  AGENT --> SIM
  SIM --> REPLAY
  EXPL --> PG
  VALUE --> PG
  DECK --> PG

  %% Async via Kafka
  MATCH --> KAFKA
  SIM --> KAFKA
  REWARD --> KAFKA
  REPLAY --> KAFKA
  BAYES --> KAFKA
  KAFKA --> SIM
  KAFKA --> REWARD
  KAFKA --> BAYES
  KAFKA --> VALUE

  %% Core ↔ Data
  CIR --> MONGO
  REPLAY --> MONGO
  REPLAY --> BLOB
  BAYES --> PG
  BAYES --> NEO
  EXPL --> NEO
  VALUE --> REDIS
  MATCH --> REDIS
  AGENT --> BLOB

  %% External data
  CIR --> SCRY

  %% Styles
  classDef app fill:#1f2430,stroke:#7a7f8a,stroke-width:1,color:#e6e6e6
  classDef data fill:#102a43,stroke:#6aa0ff,stroke-width:1,color:#e6f0ff
  classDef ext fill:#2d2436,stroke:#b18cd9,stroke-width:1,color:#f2eaff
  class INGRESS,PUBWEB,UI,VIEWER,DECK,CIR,MATCH,SIM,AGENT,HOOK,REPLAY,EXPL,VALUE,REWARD,BAYES app
  class PG,MONGO,NEO,REDIS,KAFKA,BLOB,CFG,KV data
  class USER,COMM,SCRY,IDP ext
