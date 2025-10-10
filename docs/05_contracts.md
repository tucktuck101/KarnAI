# Interface & API Contracts (v0.1)

Defines stable cross-module interfaces. These are contracts that implementations must satisfy.
Versioned by `karnai.contracts.__version__` and semver. Breaking changes bump MINOR pre-1.0.

## Namespaces
- Data Ingestion: `DataSource`, `CRLoader`, `OracleLoader`
- Engine: `RulesEngine`
- Environment: `AECEnv`, `GymEnvFacade`
- Persistence: `RunStore`
- CLI Renderer: `Renderer`
- Bot Policies: `Policy`
- Scheduler: `Scheduler`

## Error Model
- `ContractError` for pre/post-condition violations.
- `NotSupported` for unsupported capabilities.
- `DataError` for ingestion/schema failures.

## Capability Matrix
Each impl exposes `.capabilities() -> dict[str, bool]` reporting optional features:
- `"distributed"`, `"replay_bytes"`, `"vectorized_env"`, `"otlp_tracing"`, `"deterministic_step"`.

## Versioning
- `karnai.contracts.__version__` bumps MINOR for breaking changes pre-1.0.
- Contract tests guard the public surface.
