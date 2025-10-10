flowchart LR
%% System context using standard flowchart for better rendering

classDef center fill:#fff6b3,stroke:#333,stroke-width:2px,color:#111
classDef person fill:#e8f0ff,stroke:#446
classDef ext fill:#e9ffe8,stroke:#484

k[Karn.AI<br/>EDH simulation and matchmaking]:::center

subgraph People
  direction TB
  p[EDH Player]:::person
  r[Researcher / Analyst]:::person
  o[Community Node Operator]:::person
  m[Maintainer / DevOps]:::person
end

subgraph External Systems
  direction TB
  s[Card DB / Oracle]:::ext
  cr[Rules Feed]:::ext
  w[Community Simulation Clients]:::ext
end

%% Relationships
p -->|Submit decks<br/>Request matches| k
r -->|View analytics<br/>Replays| k
m -->|Operate<br/>Configure| k
o -->|Provision workers| w
w -->|Fetch jobs<br/>Return results| k

k -->|Retrieve card<br/>and legality data| s
k -->|Ingest rules<br/>updates| cr
