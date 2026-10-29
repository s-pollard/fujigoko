# service classification

This file records placement and lifecycle decisions. The [service inventory](README.md) owns deployed/target service lists, dependencies, and verified authentication. [Backups](../backups/README.md#service-priorities) owns backup priorities.

## states

- **Current / deployed:** recorded as running or in use.
- **Verified:** a specific check passed; keep its scope and date rather than implying full recovery is proven.
- **Target / planned:** intended future state, not evidence of deployment.
- **Candidate:** under consideration; purchase or deployment is not confirmed.
- **Deferred:** evaluated but postponed until a concrete requirement exists.
- **Retired / removed:** historical state, not current placement.

## placement decisions

| Workload | Decision |
| --- | --- |
| Media and manga | Keep on Kawaguchi; payloads are largely reacquirable, with configuration/metadata having greater recovery value. |
| Photos and backup storage | Keep Motosu storage/photo focused; AdGuard Home there remains a target second DNS node. |
| Personal applications | Use Yamanaka only when the application solves a home-use requirement. |
| Supporting databases/caches | Keep with the parent application and private to its Compose network unless external access is required. |
| Monitoring agents | Run on the monitored host; central monitoring/logging stays on Yamanaka. |
| Experimental workloads | Keep in gusuku; Fujigoko must not depend on them. |

See [architecture](../architecture/README.md) for the invariants behind these decisions.

## application decisions

- HomeBox remains deployed during Kept evaluation/import.
- Nextcloud is deferred, not rejected; reconsider only for a concrete file-sync/collaboration need.
- Grocy, TriliumNext, Vaultwarden, and Kept are deployed and included in the production backup path and restore verification. Exact evidence and limitations are in [backups](../backups/README.md#verified-yamanaka-to-motosu-recovery-path).
- BentoPDF is deployed on Yamanaka as the current lightweight PDF utility. The current simple deployment is stateless/redeployable and uses the existing private Caddy access path.
- Stirling PDF was retired and removed on 2026-10-29 after BentoPDF was verified through the existing private HTTPS route.
- Application authentication exceptions and verified OIDC integrations are maintained in [services](README.md#authentication).

Do not deploy an application merely because it is interesting or available. Remove ideas that are no longer useful rather than carrying them indefinitely.

## retired state

Retired Kawaguchi services, migration rollback copies, cleanup counts, and completion dates are recorded in [migration history](../history/yamanaka-migration-2026.md#retired-from-kawaguchi). Stirling PDF was retired from Yamanaka on 2026-10-29 and replaced by BentoPDF. Presence in old notes or backups does not establish active production placement.

## new services and migrations

Use the [service deployment checklist](../runbooks/service-deployment.md). Independent backup coverage and a representative restore test are required before treating new state as safely protected. Stateless/redeployable utilities may instead be documented as rebuildable when they have no persistent application state to protect.
