flowchart TD
  %% Trust boundaries
  subgraph Public_Boundary["User Boundary"]
    U[User via CLI]
  end

  subgraph KarnAI_POC["Karn.AI POC System"]
    CR[/"Rules Assets\n(MagicCompRules.txt, keywords.yml)"/]:::data
    FS[/"Artifact Store\n(JSON on NTFS)"/]:::data

    RNR[cli-runner]:::app
    MM[matchmaker V1]:::app
    DL[deck-loader]:::app
    RAD[rules-adapter]:::app
    ENG[simulation-engine]:::app
    AGT[simple-agent]:::app
    RW[replay-writer]:::app
    EVL[evaluator V1]:::app
  end

  %% Interactions
  U -->|commands| RNR
  RNR --> MM
  MM -->|deck paths| DL
  DL -->|CardIR.json| FS
  RNR -->|seed, config| ENG
  ENG --> RAD
  RAD --> CR
  ENG -->|obs->action| AGT
  ENG -->|step events| RW
  RW -->|replay.ndjson, summary.json| FS
  ENG -->|result| EVL
  EVL -->|metrics.json| FS

  %% Styles
  classDef app fill:#222,stroke:#888,stroke-width:1,color:#fff
  classDef data fill:#113355,stroke:#6aa0ff,stroke-width:1,color:#fff
